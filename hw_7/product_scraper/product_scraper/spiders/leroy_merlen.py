import scrapy
from scrapy.http import HtmlResponse
# from scrapy.loader import ItemLoader
from product_scraper.items import ProductScraperItem


class LeroyMerlenSpider(scrapy.Spider):
    name = 'leroy_merlen'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        super().__init__()
        self.start_urls = [
            f'https://leroymerlin.ru/search/?q={search}&suggest=true']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(
            '//a[contains(@aria-label, "Следующая")]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath('//a[@data-qa="product-name"]')
        for link in links:
            yield response.follow(link, callback=self.product_parse)

    def product_parse(self, response: HtmlResponse):
        # loader = ItemLoader(item=ProductScraperItem(), response=response)
        # loader.add_xpath('url', response.url)
        # loader.add_xpath('name', '//h1/text()')
        # loader.add_xpath('price', '//span[@slot="price"]/text()')
        # loader.add_xpath('parameters', '//div[@class="def-list__group"]')
        # loader.add_xpath(
        #     'images', '//picture[@slot="pictures"]/source[@media=" only '
        #               'screen and (min-width: 1024px)"]/@data-origin')
        #
        # yield loader.load_item()

        url = response.url
        name = response.xpath('//h1/text()').extract_first()
        price = response.xpath('//span[@slot="price"]/text()').extract_first()

        characteristics = {}
        parameters = response.xpath(
            '//div[@class="def-list__group"]')
        for parameter in parameters:
            key = parameter.xpath('./dt/text()').extract_first()
            value = parameter.xpath('./dd/text()').extract_first()
            characteristics[key] = value.strip()

        images = response.xpath(
            '//picture[@slot="pictures"]/source[@media=" only screen and '
            '(min-width: 1024px)"]/@data-origin').extract()

        yield ProductScraperItem(
            url=url, name=name, price=price,
            characteristics=characteristics, images=images
        )
