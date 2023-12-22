BOT_NAME = "fund_project"

SPIDER_MODULES = ["fund_project.spiders"]
NEWSPIDER_MODULE = "fund_project.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "fund_project (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True


#HTTPS_PROXY = 'https://65.18.114.254:55443'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
DEFAULT_REQUEST_HEADERS = {
    'X-Requested-With': 'XMLHttpRequest',
}

# Set rotating user agents: pip install scrapy-user-agents



# Configure a delay for requests for the same website (default: 0)
#DOWNLOAD_DELAY = 3

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Configure item pipelines
ITEM_PIPELINES = {
    "fund_project.pipelines.FundProjectPipeline": 300,
}



# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
