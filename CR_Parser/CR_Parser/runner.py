from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from CR_Parser import settings
from CR_Parser.spiders.power_tools import PowerToolsSpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(PowerToolsSpider)
    process.start()
