
import time
import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.http.response.html import HtmlResponse
from bs4 import BeautifulSoup
from util import *


class WeBikeSpider(scrapy.Spider):
    def __init__(self, name="webike", **kwargs):
        self.base_url = 'https://www.webike.vn'
        self.data = []
        self.name = name

    def start_requests(self):
        html = BeautifulSoup(requests.get("https://www.webike.vn/cho-xe-may/danh-sach-xe.html", verify=False).text, "lxml")
        max_page = 10000
        for i in range(1, max_page):
            time.sleep(0.05)
            yield scrapy.Request(
                url=f'https://www.webike.vn/cho-xe-may/danh-sach-xe.html?page={i}',
                callback=self.parse_page,
            )


    def parse_page(self, response: HtmlResponse):
        html = BeautifulSoup(response.text, "lxml")
        products = html.find_all('div', 'bike-item')
        for prod in products:
            a = prod.find('a')
            if a is not None:
                    url = a.get('href')
                    time.sleep(0.05)
                    yield scrapy.Request(
                        url=url,
                        callback=self.parse_data,
                    )

    def parse_data(self, response: HtmlResponse):
        html = BeautifulSoup(response.text, "lxml")
        name = html.find('span', class_="bottom_redline").getText().strip()
        table = html.find('table')
        price = html.find('big', class_='price').getText().strip()
        data = {
            "name": "",
            "price": "",
            "address": "",
            "information": {},
            "url": response.url
        }
        data["price"] = price
        data["name"] = name
        if table is not None:
            infos = table.findAll('td')
            if infos is not None:
                for i in range(1,len(infos),2):
                    key = infos[i-1].find('label')
                    if key is not None:
                        val = infos[i].getText().strip().strip()
                        data["information"][key.getText().strip()] = val

        self.data.append(data)
        producer_send(self.name, data)

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
        # print(data)
        pd.DataFrame(data).to_excel(
            f"./data/muaban.xlsx", index=False, sheet_name="data")
        return


def main() -> None:
    process = CrawlerProcess()
    process.crawl(WeBikeSpider)
    process.start()


if __name__ == "__main__":
    main()
