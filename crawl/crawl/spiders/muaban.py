
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http.response.html import HtmlResponse
from bs4 import BeautifulSoup
from util import make_request


class MuaBanSpider(scrapy.Spider):
    def __init__(self, name="muabn-spider", **kwargs):
        self.base_url = 'https://muaban.net'
        self.data = []

    def start_requests(self):
        # for i in range(1, 30):

        for i in range(1, 2):
            data = make_request(
                self.base_url+f"/listing/v1/classifieds/listing?category_id=35&limit=20&offset={i}")
            if data is None:
                print(f"Failed to retrieve data")
                continue
            products = data.get("items")
            for prod in products:
                url = prod.get("url")
                if url is None:
                    continue
                # time.sleep(0.05)
                yield scrapy.Request(
                    url=self.base_url+url,
                    callback=self.parse_data,
                )

    def parse_data(self, response: HtmlResponse):
        html = BeautifulSoup(response.text, "lxml")
        name = html.find("div", class_="klItbj").find("h1").text
        price = html.find("div", class_="klItbj").find("div", class_="price").text
        address = html.find("div", class_="klItbj").find("div", class_="address").text

        # brand = html.find("div", class_="gqfnhz").find("span").text
        # vehicle = html.find("div", class_="eShBuU").find("span").text
        # status = html.find("div", class_="jSMHJP").find("span").text
        # type = html.find("div", class_="neMoc").find("span").text
        # capacity = html.find("div", class_="jJIaaY").find("span").text
        # color = html.find("div", class_="fyjlpY").find("span").text
        # source = html.find("div", class_="iMdtLg").find("span").text
        # used = html.find("div", class_="kFRjSs").find("span").text
        # year_register = html.find("div", class_="bjnWfw").find("span").text
        
        print(name, price, address)
        # , brand, vehicle, status, type, capacity, color, source, used, year_register)
        # bắn kafka

    def closed(self, reason):
        pass


def main() -> None:
    process = CrawlerProcess()
    process.crawl(MuaBanSpider)
    process.start()


if __name__ == "__main__":
    main()
