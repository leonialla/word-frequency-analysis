import re
import scrapy
import requests

from urllib.parse import urljoin
from news.items import NewsItem


PAGES_REGEX = re.compile(r".*?\/(\d+)", re.DOTALL)
ARTICLE_INFO_REGEX = re.compile(
    r"^(?P<published_at>[\d\s\-:]+)\s[图文、/来源：]*(?P<author>.*?)\s点击：\[\]",
    re.DOTALL,
)
GET_CLICKS_SCRIPT_REGEX = re.compile(
    r"^_showDynClicks\(\"(?P<click_type>\w+)\", (?P<owner>\d+), (?P<click_id>\d+)\)$"
)


class NewsSpider(scrapy.Spider):
    name = "news"
    start_urls = [
        "https://www.sust.edu.cn/xxyw/yxz1.htm",
    ]

    def parse(self, response):
        statistics = response.css(
            "body table tr:last-child table table td:first-child::text"
        ).extract_first()
        pages = int(PAGES_REGEX.match(statistics).group(1))
        links = response.css(
            "body .neirong-content table tr:not(:last-child) a::attr(href)"
        ).extract()

        for link in links:
            yield response.follow(urljoin(response.url, link), self.resolve_news_detail)

        for page in range(1, pages):
            yield response.follow(
                f"https://www.sust.edu.cn/xxyw/yxz1/{page}.htm", self.parse
            )

    def resolve_news_detail(self, response):
        title = response.css(
            "body [name=_newscontent_fromname] h1::text"
        ).extract_first()

        info = "".join(
            response.css(
                "body [name=_newscontent_fromname] div div:nth-child(4)::text"
            ).extract()
        )
        published_at, author = ARTICLE_INFO_REGEX.match(info).groups()

        get_clicks_script = response.css(
            "body [name=_newscontent_fromname] div div:nth-child(4) script::text"
        ).extract_first()
        click_type, owner, click_id = GET_CLICKS_SCRIPT_REGEX.match(
            get_clicks_script
        ).groups()
        clicks = requests.get(
            "https://www.sust.edu.cn/system/resource/code/news/click/dynclicks.jsp?",
            params={
                "clickid": click_id,
                "owner": owner,
                "clicktype": click_type,
            },
        ).text

        content = "".join(
            response.css(
                "body .newstext p::text, body .newstext p span::text, body .newstext p strong::text"
            ).extract()
        ).replace("\xa0", "")
        image_urls = [
            urljoin("https://www.sust.edu.cn", url)
            for url in response.css("body .newstext img::attr(src)").extract()
        ]

        yield NewsItem(
            title=title,
            author=author,
            published_at=published_at,
            clicks=int(clicks),
            content=content,
            image_urls=image_urls,
        )
