import json
import logging

from news.models import Session, News


class NewsPipeline:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def open_spider(self, _):
        self.session = Session()
        self.logger.info(
            f"Established connection to database successfully. Connection URL: {self.session.bind.url}."
        )

    def close_spider(self, _):
        self.session.close()
        self.logger.info("Closed connection from database.")

    def process_item(self, item, _):
        self.session.add(
            News(
                **{key: item[key] for key in item if key != "image_urls"},
                image_urls=",".join(item["image_urls"]),
            )
        )
        self.session.commit()
        self.logger.info(
            json.dumps(
                {
                    "title": item["title"],
                    "author": item["author"],
                },
                ensure_ascii=False,
            )
        )
        return item
