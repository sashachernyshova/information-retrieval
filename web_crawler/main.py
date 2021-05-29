import time
from web_crawler.classes.webcrawler import WebCrawler


def main():
    start_time = time.time()
    crawler = WebCrawler()
    res = crawler.multi_run(
        number_of_pages=10,
        starting_idx=470000,
        time_between=0.5,
        num_of_processes=8,
    )
    total = time.time() - start_time
    print(total)

    crawler.data2csv(res)


if __name__ == "__main__":
    main()
