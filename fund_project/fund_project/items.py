import scrapy

class FundProjectItem(scrapy.Item):
    isin = scrapy.Field()
    document_type = scrapy.Field()
    effective_date = scrapy.Field()
    file_size = scrapy.Field()
    download_url = scrapy.Field()