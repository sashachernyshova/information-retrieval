class Author:
    """Class contains info about author

    FUNCTIONS:
        init: Following entities are got from get_author_info function
            author_name (str)
            author_nickname (str)
            author_karma (str)
            author_rating (str)
            author_specialization (str)


        get_author_info:
            Habr has two types of posts: post and megapost. Megapost has different type of html tags,
            that is why there are several try blocks in some places.

            Input: soup

            Returns: tuple(str)
    """

    def __init__(self, soup):
        (
            self.author_name,
            self.author_nickname,
            self.author_karma,
            self.author_rating,
            self.author_specialization,
        ) = self.get_author_info(soup)

    def get_author_info(self, soup):
        try:
            author_name = soup.find(
                "a", {"class": "user-info__fullname"}
            ).get_text(" ", strip=True)
        except Exception:
            author_name = None

        try:
            author_nickname = soup.find(
                "a", {"class": "user-info__nickname"}
            ).get_text(" ", strip=True)
        except Exception:
            try:
                author_nickname = "MEGAPOST"
                author_name = soup.find(
                    "a", {"class": "megapost-head__blog-link"}
                ).get_text(" ", strip=True)
            except Exception:
                author_nickname = None

        try:
            author_karma = (
                soup.find("a", {"class": "user-info__stats-item stacked-counter"})
                .get_text(" ", strip=True)
                .split()[0]
            )
        except Exception:
            author_karma = None

        try:
            author_rating = (
                soup.find(
                    "a",
                    {
                        "class": "user-info__stats-item stacked-counter stacked-counter_rating"
                    },
                )
                .get_text(" ", strip=True)
                .split()[0]
            )
        except Exception:
            author_rating = None

        try:
            author_specialization = soup.find(
                "div", {"class": "user-info__specialization"}
            ).get_text(" ", strip=True)
        except Exception:
            author_specialization = None

        return (
            author_name,
            author_nickname,
            author_karma,
            author_rating,
            author_specialization,
        )
