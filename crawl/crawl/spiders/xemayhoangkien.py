
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http.response.html import HtmlResponse
from bs4 import BeautifulSoup


class XeMayHoangKienSpider(scrapy.Spider):
    def __init__(self, name="xemayhoangkien-spider", **kwargs):
        self.base_url = 'https://xemayhoangkien.com'
        self.data = []

    def start_requests(self):
        # for i in range(1, 30):
        for i in range(1, 2):
            print(i)
            # time.sleep(0.05)
            yield scrapy.Request(
                url=f'https://xemayhoangkien.com/all?page={i}',
                callback=self.parse_page,
            )

    def parse_page(self, response: HtmlResponse):
        html = BeautifulSoup(response.text, "lxml")
        products = html.findAll("div", class_="single-product")
        for prod in products:
            a = prod.find("h2", class_="product-name").find("a")
            if a is not None:
                url = a.get('href')
                # time.sleep(0.05)
                yield scrapy.Request(
                    url=self.base_url + url,
                    callback=self.parse_data,
                )

    def parse_data(self, response: HtmlResponse):
        html = BeautifulSoup(response.text, "lxml")
        name = html.find("form", id="add-to-cart-form").find("h1").text
        metadata = html.find(
            "form", id="add-to-cart-form").find("div", "product-meta").findAll("a")
        brand = metadata[0].text
        type = metadata[1]
        code = metadata[2]
        year_register = metadata[3]
        capacity = metadata[4]
        color = metadata[5]
        print(name, brand)
        # bắn kafka

    def closed(self, reason):
        pass


def main() -> None:
    process = CrawlerProcess()
    process.crawl(XeMayHoangKienSpider)
    process.start()


if __name__ == "__main__":
    main()
