import re
import scrapy
import requests

from urllib.parse import urljoin
from news.items import NewsItem


PAGES_REGEX = re.compile(r"^.*?\/(?P<pages>\d+)\s$", re.DOTALL)
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
        statistics = response.xpath(
            "//body//table//tr[last()]//table//table//td[1]/text()"
        ).extract_first()
        pages = int(PAGES_REGEX.match(statistics).group(1))
        links = response.xpath(
            "//body//*[contains(@class, 'neirong-content')]//table/tr[position() != last()]//a/@href"
        ).extract()

        for link in links:
            yield response.follow(urljoin(response.url, link), self.resolve_news_detail)

        for page in range(1, pages):
            yield response.follow(
                f"https://www.sust.edu.cn/xxyw/yxz1/{page}.htm", self.parse
            )

    def resolve_news_detail(self, response):
        title = response.xpath(
            "//body//*[@name='_newscontent_fromname']//h1/text()"
        ).extract_first()

        info = "".join(
            response.xpath(
                "//body//*[@name='_newscontent_fromname']//div/div[3]/text()"
            ).extract()
        )
        published_at, author = ARTICLE_INFO_REGEX.match(info).groups()

        get_clicks_script = response.xpath(
            "//body//*[@name='_newscontent_fromname']//div/div[3]/script/text()"
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
            response.xpath(
                "//body//*[contains(@class, 'newstext')]//p/text() | //body//*[contains(@class, 'newstext')]//p//span/text() | //body//*[contains(@class, 'newstext')]//p//strong/text()"
            ).extract()
        ).replace("\xa0", "")
        image_urls = [
            urljoin("https://www.sust.edu.cn", url)
            for url in response.xpath("//body//*[contains(@class, 'newstext')]//img/@src").extract()
        ]

        yield NewsItem(
            title=title,
            author=author,
            published_at=published_at,
            clicks=int(clicks),
            content=content,
            image_urls=image_urls,
        )
