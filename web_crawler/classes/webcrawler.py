import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, Future
from web_crawler.classes.post import Post
from web_crawler.fun.utils import clean
from time import sleep
import csv


class WebCrawler:
    """ WebCrawler for Habr parsing. Parsing starts on page with starting_index and goes backwards.
        For every page we save post's entities in all_posts (list). After finishing parsing we call data2csv function.

    FUNCTIONS:
        parse_page
            Get page by index and if we get 200 status code we check length of post.
            If it is more than 2000 we clean text and check the length again.

            Input: index

            Return: tuple with post's entities

        data2csv
            Save data to csv file

            Input: tuple with entities

            Return: csv file in working directory

         multi_run
            Multiprocessed parsing.

            Input:
                number_of_pages (int) - number of wanted pages
                starting_idx (int) - starting page for parsing
                time_between (float/int) - time gap
                num_of_processes (int) - number of processes

            Return: all_posts (list(list)) - list with lists that contain information about posts
    """

    def __init__(self):
        pass

    def parse_page(self, index):
        url = f"https://habr.com/ru/post/{index}/"
        page = requests.get(url, timeout=5)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            post_text = soup.find("div", {"id": "post-content-body"}).get_text(
                " ", strip=True
            )

            if len(post_text) > 2000:
                clean_text = clean(post_text)

                if len(clean_text) > 2000:
                    post = Post(index, soup, post_text, clean_text)
                    return post.get_entities()
        return []

    def data2csv(self, data):
        our_columns = (
            "post_index",
            "author_name",
            "author_nickname",
            "author_karma",
            "author_rating",
            "author_specialization",
            "post_title",
            "post_date",
            "post_rate",
            "post_total_votes",
            "post_saved",
            "post_seen",
            "post_num_comments",
            "post_hubs",
            "post_tags",
            "raw_post_text",
            "clean_text",
        )
        data = [our_columns] + data
        with open('parsing_results.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(data)

        print("Writing complete")

    def multi_run(
        self,
        number_of_pages,
        starting_idx,
        time_between,
        num_of_processes,
    ):
        all_posts = []
        page_idx = starting_idx
        executor = ThreadPoolExecutor(max_workers=num_of_processes)

        counter = 0
        while counter < number_of_pages:
            futures = []
            for thr in range(num_of_processes):
                futures.append(executor.submit(self.parse_page, page_idx - thr))

            for thr in range(num_of_processes):
                res = futures[thr].result()
                if len(res) != 0:
                    counter += 1
                    all_posts.append(res)
                    print("Parsed pages: "+str(counter))

                sleep(time_between)
            page_idx -= num_of_processes

        print("Finish")
        return all_posts
