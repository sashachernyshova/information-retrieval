import re
from web_crawler.classes.author import Author
import datetime


class Post:
    def __init__(self, soup, post_text, clean_text):
        post_area = soup.find("div", {"class": "post__wrapper"})
        additional_area = soup.find("div", {"class": "post-additionals"})
        self.title = soup.find('title').get_text(" ", strip=True)
        self.author = Author(soup)
        (
            self.post_date,
            self.post_rate,
            self.post_total_votes,
            self.post_saved,
            self.post_seen,
            self.post_num_comments,
            self.post_hubs,
            self.post_tags,
        ) = self.get_post_meta(post_area, additional_area)
        self.post_text = post_text
        self.clean_text = clean_text

    def get_post_meta(self, post_area, add_area):
        date = post_area.find("span", {"class": "post__time"})
        date = datetime.datetime.strptime(
            date.get("data-time_published"), "%Y-%m-%dT%H:%MZ"
        )
        rate = add_area.find("span", {"class": "voting-wjt__counter"}).get_text()
        temp = add_area.find("span")
        total_votes = re.sub("\D", " ", temp.attrs['onclick']).split()[0]
        saved = add_area.find(
            "span", {"class": "bookmark__counter js-favs_count"}
        ).get_text()
        seen = add_area.find("span", {"class": "post-stats__views-count"}).get_text()
        try:
            num_comments = add_area.find(
                "span", {"class": "post-stats__comments-count"}
            ).get_text()
        except Exception:
            num_comments = 0

        hubs = []
        tags = []

        temp = post_area.find(
            "ul", {"class": "inline-list inline-list_fav-tags js-post-hubs"}
        ).findChildren("a")
        for hub in temp:
            hubs.append(hub.text.strip())

        temp = post_area.find(
            "ul", {"class": "inline-list inline-list_fav-tags js-post-tags"}
        ).findChildren("a")
        for tag in temp:
            tags.append(tag.text.strip())

        return date, rate, total_votes, saved, seen, num_comments, hubs, tags

    def get_entities(self):
        return [
            self.author.author_name,
            self.author.author_nickname,
            self.author.author_karma,
            self.author.author_rating,
            self.author.author_specialization,
            self.title,
            self.post_date,
            self.post_rate,
            self.post_total_votes,
            self.post_saved,
            self.post_seen,
            self.post_num_comments,
            self.post_hubs,
            self.post_tags,
            self.post_text,
            self.clean_text,
        ]
