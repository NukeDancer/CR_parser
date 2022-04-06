# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from typing import Union

import scrapy

from itemloaders.processors import Compose, TakeFirst


def process_price(raw_price) -> Union[float, list]:
    try:
        price = raw_price[0].replace(' ', '')
        return float(price)
    except Exception:
        return raw_price


class CrParserItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=Compose(process_price), output_processor=TakeFirst())
    image_urls = scrapy.Field()
    images = scrapy.Field()
    _id = scrapy.Field()
