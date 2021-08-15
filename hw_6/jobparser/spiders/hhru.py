import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = {'https://hh.ru/search/vacancy?area=&fromSearchLine='
                  'true&st=searchVacancy&text=python'}

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(
            '//a[@data-qa="pager-next"]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath(
            '//a[@data-qa="vacancy-serp__vacancy-title"]/@href').extract()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        url = response.url
        name = response.xpath('//h1/text()').extract_first()
        salary_min = response.xpath(
            '//p[@class="vacancy-salary"]/span/text()').extract_first()
        # salary_from = response.css(
        #     'p.vacancy-salary span::text').extract_first()
        salary_max = salary_min
        currency = salary_min
        site = self.allowed_domains[0]

        yield JobparserItem(
            url=url, name=name, salary_min=salary_min,
            salary_max=salary_max, currency=currency, site=site
        )
