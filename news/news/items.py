import scrapy


class NewsItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    published_at = scrapy.Field()
    clicks = scrapy.Field()
    content = scrapy.Field()
    image_urls = scrapy.Field()
