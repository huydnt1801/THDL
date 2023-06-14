from scrapy.crawler import CrawlerProcess
from apscheduler.schedulers.twisted import TwistedScheduler
from muaban import MuaBanSpider
from xemayhoangkien import XeMayHoangKienSpider

process = CrawlerProcess()


def start_crawl():
    process.crawl(MuaBanSpider)
    process.crawl(XeMayHoangKienSpider)


start_crawl()
scheduler = TwistedScheduler()
scheduler.add_job(start_crawl, 'interval', minutes=5)
scheduler.start(paused=False)
process.start(False)
