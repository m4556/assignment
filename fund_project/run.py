from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from fund_project.settings import *  # Import your settings from fund_project.settings
from fund_project.spiders.fund import FundSpider

def run_spider():
    custom_settings = {
        'BOT_NAME': 'fund_project',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'NEWSPIDER_MODULE': 'fund_project.spiders',
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',
        'ROBOTSTXT_OBEY': True,
        'SPIDER_MODULES': ['fund_project.spiders'],
        'TWISTED_REACTOR': 'twisted.internet.asyncioreactor.AsyncioSelectorReactor',
         # user agent
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 '
                      'Safari/537.36',
        'DEFAULT_REQUEST_HEADERS': {
            'X-Requested-With': 'XMLHttpRequest',
        },
        'ITEM_PIPELINES': {
            "fund_project.pipelines.FundProjectPipeline": 300,
        },
    }

    settings = Settings()
    settings.setdict(custom_settings)

    process = CrawlerProcess(settings)
    process.crawl(FundSpider)
    process.start()

if __name__ == "__main__":
    run_spider()
