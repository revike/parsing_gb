from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from hw_6.jobparser import settings
from hw_6.jobparser.spiders import hhru, superjob

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(hhru.HhruSpider)
    process.crawl(superjob.SuperjobSpider)

    process.start()
