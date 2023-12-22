import scrapy
import json
import re
import os
from urllib.parse import urljoin, urlparse, urlencode
from ..items import FundProjectItem


class FundSpider(scrapy.Spider):
    name = "fund"
    url = 'https://fondswelt.hansainvest.com/en/download-center'
    base_url = 'https://fondswelt.hansainvest.com/en/download-center/datatable'
    num_data = 200

    def __init__(self):
        self.count = 0
        self.page_number=0

    def start_requests(self):
        url = self.base_url
        data = {
            'columns[0][data]': 0,
            'columns[0][name]': '',
            'columns[0][searchable]': True,
            'columns[0][orderable]': True,
            'columns[0][search][value]': '',
            'columns[0][search][regex]': False,

            'columns[1][data]': 1,
            'columns[1][name]': '',
            'columns[1][searchable]': True,
            'columns[1][orderable]': True,
            'columns[1][search][value]': '',
            'columns[1][search][regex]': False,

            'columns[2][data]': 2,
            'columns[2][name]': '',
            'columns[2][searchable]': True,
            'columns[2][orderable]': True,
            'columns[2][search][value]': '',
            'columns[2][search][regex]': False,

            'columns[3][data]': 3,
            'columns[3][name]': '',
            'columns[3][searchable]': True,
            'columns[3][orderable]': True,
            'columns[3][search][value]': '',
            'columns[3][search][regex]': False,

            'columns[4][data]': 4,
            'columns[4][name]': '',
            'columns[4][searchable]': True,
            'columns[4][orderable]': True,
            'columns[4][search][value]': '',
            'columns[4][search][regex]': False,

            'columns[5][data]': 5,
            'columns[5][name]': '',
            'columns[5][searchable]': True,
            'columns[5][orderable]': True,
            'columns[5][search][value]': '',
            'columns[5][search][regex]': False,

            'order[0][column]': 0,
            'order[0][dir]': 'asc',

            'start': 0,
            'length': 25,

            'search[value]': '',
            'search[regex]': False,
            'search[fund]': '',
            'search[country]': '',

            '_': 1703192905374
        }

        yield scrapy.Request(url, meta={'data': data}, callback=self.parse)


    def parse(self, response):
        data = json.loads(response.text)

        for row in data['data']:
            raw_name = row[0]
            raw_docs = row[1:]

            identifier_match = re.search(r'<span class="d-block">([^<]+)</span>', raw_name)
            identifier = identifier_match.group(1).strip() if identifier_match else None

            for raw_doc in raw_docs[:3]:

                # document types can be extracted from sending request to orig. page  response.css('table.data-table thead th::text').extract() or pdf url ext
                doc_type_matches = re.findall(r'verkaufsprospekt|jahresbericht|halbjahresbericht', raw_doc, re.I)
                doc_type = doc_type_matches[0] if doc_type_matches else None

                match = re.search(r'href="(.+?)"', raw_doc)
                d_url = match.group(1) if match else None
                download_url = urljoin(self.url, d_url)

                match = re.search(r'<span class="d-block">(.+)</span>', raw_doc)
                date = match.group(1) if match else None

                match = re.search(r'<small class="d-block">(.+)</small>', raw_doc)
                size = match.group(1) if match else None

                if d_url and self.count < self.num_data:
                    yield FundProjectItem(
                     isin= identifier,
                     document_type=doc_type,
                     download_url= download_url,
                     effective_date= date,
                     file_size= size
                    )
                    self.count += 1
                    print("count aaa", self.count)

        if self.count < self.num_data:

            start_value = self.page_number * 25
            response.meta['data']['start'] = start_value
            params = urlencode(response.meta['data'])
            next_page_url = f"{self.base_url}?{params}"
            yield scrapy.Request(next_page_url, meta=response.meta, callback=self.parse)
            self.page_number += 1