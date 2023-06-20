
import time
import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.http.response.html import HtmlResponse
from bs4 import BeautifulSoup
from util import *


class MuaBanSpider(scrapy.Spider):
    def __init__(self, name="muaban", **kwargs):
        self.base_url = 'https://muaban.net'
        self.data = []
        self.name = name

    def start_requests(self):
        data = make_request(
            self.base_url+f"/listing/v1/classifieds/listing?category_id=35&limit=1")
        # total = data.get("total")
        total = 25
        i = 20
        while i < total:
            time.sleep(0.2)
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
                time.sleep(0.05)
                yield scrapy.Request(
                    url=self.base_url+url,
                    callback=self.parse_data,
                    meta={"name": prod.get("title"), "price": prod.get("price")}
                )
            i += 20

    def parse_data(self, response: HtmlResponse):
        html = BeautifulSoup(response.text, "lxml")
        base_info = html.find("div", class_="klItbj")
        data = {
            "name": response.request.meta["name"],
            "price": response.request.meta["price"],
            "address": "",
            "information": {},
            "url": response.url,
            "image_url": ""
        }
        if base_info is not None:
            if data["name"] == "" and base_info.find("h1") is not None:
                data["name"] = base_info.find("h1").getText()
            if data["price"] == "" and base_info.find("div", class_="price") is not None:
                data["price"] = base_info.find("div", class_="price").getText()
            if base_info.find("div", class_="address") is not None:
                data["address"] = base_info.find(
                    "div", class_="address").getText()
            if data["image_url"] == "" and html.find("div", class_="kzipBv") is not None:
                link = html.find("div", class_="kzipBv")
                data["image_url"] = link.find("img")['src']

        information = html.find("ul", class_="hhzOAT")
        if information is not None:
            infos = information.findAll("li")
            for info in infos:
                key, value = info.getText().split(":")
                data["information"][key] = value

        self.data.append(data)
        producer_send(self.name, data)

    def closed(self, reason):
        print(reason)
        data = {
            "name": [],
            "price": [],
            "address": [],
            "information": [],
            "url": [],
            "image_url": [],
        }
        for i in self.data:
            data["name"].append(i["name"])
            data["price"].append(i["price"])
            data["address"].append(i["address"])
            data["information"].append(json.dumps(
                i["information"], ensure_ascii=False))
            data["url"].append(i["url"])
            data["image_url"].append(i["image_url"])
        # pd.DataFrame(data).to_excel(
        #     f"./data/muaban.xlsx", index=False, sheet_name="data")
        return


def main() -> None:
    process = CrawlerProcess()
    process.crawl(MuaBanSpider)
    process.start()


if __name__ == "__main__":
    main()
