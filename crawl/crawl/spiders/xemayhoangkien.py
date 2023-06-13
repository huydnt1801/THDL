
import time
import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.http.response.html import HtmlResponse
from bs4 import BeautifulSoup
from util import *


class XeMayHoangKienSpider(scrapy.Spider):
    def __init__(self, name="xemayhoangkien-spider", **kwargs):
        self.base_url = 'https://xemayhoangkien.com'
        self.data = []
        self.name = name

    def start_requests(self):
        for i in range(1, 29):
            time.sleep(0.05)
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
                time.sleep(0.05)
                yield scrapy.Request(
                    url=self.base_url + url,
                    callback=self.parse_data,
                )

    def parse_data(self, response: HtmlResponse):
        html = BeautifulSoup(response.text, "lxml")
        form = html.find("form", id="add-to-cart-form")
        data = {
            "name": "",
            "price": "",
            "address": "",
            "information": {},
            "url": response.url
        }
        if form is not None:
            data["name"] = form.find("h1").getText()
            data["price"] = form.find("span", class_="special-price").getText()
            metadata = form.find("div", "product-meta")
            if metadata is not None:
                infos = metadata.findAll("span")
                for info in infos:
                    key, val = process_string(info.getText()).split(":")
                    data["information"][key] = val

        self.data.append(data)
        # bắn kafka

    def closed(self, reason):
        print(reason)
        data = {
            "name": [],
            "price": [],
            "address": [],
            "information": [],
            "url": []
        }
        for i in self.data:
            data["name"].append(i["name"])
            data["price"].append(i["price"])
            data["address"].append(i["address"])
            data["information"].append(json.dumps(
                i["information"], ensure_ascii=False))
            data["url"].append(i["url"])
        pd.DataFrame(data).to_excel(
            f"./data/xemayhoangkien.xlsx", index=False, sheet_name="data")
        return


def main() -> None:
    process = CrawlerProcess()
    process.crawl(XeMayHoangKienSpider)
    process.start()


if __name__ == "__main__":
    main()
