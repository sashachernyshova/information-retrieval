import re
from web_crawler.classes.author import Author
import datetime


class Post:
    """Class contains info about posts

    FUNCTIONS:
        init:
            post_index (int)
            title (str)
            author (Author class object)
            post_text (str)
            clean_text (str)

            Following entities are got from get_post_meta function:
                post_date (datetime)
                post_rate (str)
                post_total_votes (str) - total number of rating votes
                post_saved (str)
                post_seen (str)
                post_num_comments (str)
                post_hubs list(str)
                post_tags list(str)


        get_post_meta
            Habr has two types of posts: post and megapost. Megapost has different type of html tags,
            that is why there are several try blocks in some places.

            Input: soup

            Returns: tuple


        get_entities
            Returns all object's entities
    """

    def __init__(self, index, soup, post_text, clean_text):
        self.post_index = index
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
        ) = self.get_post_meta(soup)
        self.post_text = post_text
        self.clean_text = clean_text

    def get_post_meta(self, soup):
        try:
            date = soup.find("span", {"class": "post__time"})
            date = datetime.datetime.strptime(
                date.get("data-time_published"), "%Y-%m-%dT%H:%MZ"
            )
        except Exception:
            try:
                temp = soup.find("div", {"class": "megapost-head__meta"})
                temp = temp.find_all("li", {"class": "list__item"})
                date = datetime.datetime.strptime(
                    temp.get("data-time_published"), "%Y-%m-%dT%H:%MZ"
                )
            except Exception:
                date = None
        rate = soup.find("span", {"class": "voting-wjt__counter"}).get_text()

        temp = soup.find_all("span", {"class": "voting-wjt__counter"})
        total_votes = re.sub("\D", " ", temp[0].attrs['onclick']).split()[0]

        saved = soup.find(
            "span", {"class": "bookmark__counter js-favs_count"}
        ).get_text()
        seen = soup.find("span", {"class": "post-stats__views-count"}).get_text()
        try:
            num_comments = soup.find(
                "span", {"class": "post-stats__comments-count"}
            ).get_text()
        except Exception:
            num_comments = 0

        hubs = []
        tags = []
        try:
            temp = soup.find(
                "ul", {"class": "inline-list inline-list_fav-tags js-post-hubs"}
            ).findChildren("a")
        except Exception:
            temp = soup.find(
                "ul", {"class": "megapost-head__hubs list list_inline"}
            ).findChildren("a")
        finally:
            for hub in temp:
                hubs.append(hub.text.strip())

        temp = soup.find(
            "ul", {"class": "inline-list inline-list_fav-tags js-post-tags"}
        ).findChildren("a")
        for tag in temp:
            tags.append(tag.text.strip())

        return date, rate, total_votes, saved, seen, num_comments, hubs, tags

    def get_entities(self):
        return [
            self.post_index,
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
