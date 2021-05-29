class Author:
    def __init__(self, post_info):
        (
            self.author_name,
            self.author_nickname,
            self.author_karma,
            self.author_rating,
            self.author_specialization,
        ) = self.get_author_info(post_info)

    def get_author_info(self, post_info):
        try:
            author_name = post_info.find(
                "a", {"class": "user-info__fullname"}
            ).get_text(" ", strip=True)
        except Exception:
            author_name = None

        try:
            author_nickname = post_info.find(
                "a", {"class": "user-info__nickname"}
            ).get_text(" ", strip=True)
        except Exception:
            try:
                author_nickname = "MEGAPOST"
                author_name = post_info.find(
                    "a", {"class": "megapost-head__blog-link"}
                ).get_text(" ", strip=True)
            except Exception:
                author_nickname = None

        try:
            author_karma = (
                post_info.find("a", {"class": "user-info__stats-item stacked-counter"})
                .get_text(" ", strip=True)
                .split()[0]
            )
        except Exception:
            author_karma = None

        try:
            author_rating = (
                post_info.find(
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
            author_specialization = post_info.find(
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
