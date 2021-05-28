import time
from web_crawler.classes.webcrawler import WebCrawler

def main():
    start_time = time.time()
    crawler = WebCrawler()
    resus = crawler.multi_run()
    total = time.time() - start_time
    print(total)
