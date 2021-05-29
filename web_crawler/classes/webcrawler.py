import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, Future
from web_crawler.classes.post import Post
from web_crawler.fun.utils import clean
from time import sleep
import csv


class WebCrawler:
    def __init__(self):
        pass

    def parse_page(self, index):
        url = f"https://habr.com/ru/post/{index}/"
        page = requests.get(url)
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

        with open("posts.csv", "w") as f:
            writer = csv.writer(f)
            #             writer.writerow(our_columns)
            writer.writerow((data))

    def multi_run(
        self,
        number_of_pages=10,
        starting_idx=500000,
        time_between=0.5,
        num_of_processes=3,
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

                sleep(time_between)
            page_idx -= num_of_processes

        print("Finish")
        return all_posts
