
import time
import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.http.response.html import HtmlResponse
from bs4 import BeautifulSoup
from util import *


class OkXeSpider(scrapy.Spider):
    def __init__(self, name="muaban", **kwargs):
        self.base_url = 'https://api.okxe.vn'
        self.web_url = 'https://www.okxe.vn'
        self.data = []
        self.name = name

    def start_requests(self):
        i = 1
        max_page = 18
        while i <= max_page:
            time.sleep(0.2)
            data = make_request(
                self.base_url+f"/api/v2/products?page={i}&per_page=20")
            # print(data)
            if data is None:
                print(f"Failed to retrieve data")
                continue
            products = data.get("data")
            for prod in products:
                # print(prod["q_product_name"])
                url = f"/api/v2/products/{prod['id']}"
                print(url)
                if url is None:
                    continue
                time.sleep(0.05)
                yield scrapy.Request(
                    url=self.base_url+url,
                    callback=self.parse_data,
                    meta={"name": prod.get("q_product_name"), "price": prod.get("price")}
                )
            i += 1

    def parse_data(self, response: HtmlResponse):
        product = response.json().get('data')
        print(product['product_name'])
        data = {
            "name": product["product_name"],
            "price": product["price"],
            "address": "",
            "information": {},
            "url": self.web_url + f"/products/{product.get('bike_slug')}-{product.get('id')}"
        }

        data["information"]["brand"] = product['brand'].get('name')
        data["information"]["image_url"] = product['image'].get('large')
        data["information"]["model"] = product['model'].get('name')
        data["information"]["store"] = product['store'].get('name')
        data['address'] = product['location'].get('name')
        data["information"]["type"] = product.get('type')
        data["information"]["fuel"] = product['detail_model'].get('fuel')
        data["information"]["used_status"] = product.get('used_status')
        data["information"]["used_distance"] = product.get('used_distance')
        details = product['detail_model'].get("model_spec_selects")
        for detail in details:
            key = detail.get('name')
            value = ','.join([d.get('name') for d in detail.get('model_spec_detail_selects')])
            data['information'][key] = value


        self.data.append(data)
        # producer_send(self.name, data)

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
            f"./data/okxe.xlsx", index=False, sheet_name="data")
        return


def main() -> None:
    process = CrawlerProcess()
    process.crawl(OkXeSpider)
    process.start()


if __name__ == "__main__":
    main()
