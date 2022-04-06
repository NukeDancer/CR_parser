import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from CR_Parser.items import CrParserItem


class PowerToolsSpider(scrapy.Spider):
    name = 'power_tools'
    allowed_domains = ['www.castorama.ru']
    start_urls = ['https://www.castorama.ru/tools/power-tools']

    def parse(self, response):
        next_page = response.xpath('//a[@class="next i-next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//a[@class="product-card__name ga-product-card-name"]/@href')
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=CrParserItem(), response=response)
        loader.add_xpath('name', "//h1[@class='product-essential__name hide-max-small']/text()")
        loader.add_xpath('price', "//div[@class='product-buy-panel scrollbar-margin js-fixed-panel']//span[@class='price']/span/span/text()")
        loader.add_value('url', response.url)
        loader.add_xpath('image_urls', "//img[@class='top-slide__img swiper-lazy']/@data-src")
        yield loader.load_item()
