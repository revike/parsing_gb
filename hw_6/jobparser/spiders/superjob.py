import scrapy
from scrapy.http import HtmlResponse

from jobparser.items import JobparserItem


class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@rel="next"]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath(
            '//div[@class="f-test-search-result-item"]//a'
            '[contains(@href, "/vakansii/")]/@href').extract()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        url = response.url
        name = response.xpath('//h1/text()').extract_first()
        salary_min = response.xpath(
            '//div[contains(@class, "_3MVeX")]//span'
            '[contains(@class, "_1h3Zg _2Wp8I")]/text()').extract()
        salary_max = salary_min
        currency = salary_min
        site = self.allowed_domains[0]

        yield JobparserItem(
            url=url, name=name, salary_min=salary_min,
            salary_max=salary_max, currency=currency, site=site
        )
