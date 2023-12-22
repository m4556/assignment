import os
import csv
import requests
import hashlib
from scrapy.exceptions import DropItem
from datetime import datetime
from urllib.parse import urljoin, urlparse

class FundProjectPipeline:

    def open_spider(self, spider):
        self.script_directory = os.path.dirname(os.path.abspath(__file__))
        self.fund_database_dir = os.path.join(self.script_directory, 'FundDatabase')
        os.makedirs(self.fund_database_dir, exist_ok=True)


    def process_item(self, item, spider):
        csv_path = os.path.join(self.fund_database_dir, 'fundDatabase.csv')
        with open(csv_path, 'a+', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Check header and write if needed
            if not csv_file.tell():
                csv_writer.writerow(["isin", "document_type", "effective_date", "file_size", "file_path", "download_url", "download_date", "md5_hash"])

            if self.check_existing_data(csv_file, item):
                return DropItem

            # Create ISIN folders
            #website_name = '.'.join(urlparse(item['download_url']).netloc.split('.')[:-2])
            website_name = urlparse(item['download_url']).netloc.split('.')[-2]
            isin_folder = os.path.join(self.fund_database_dir, str(website_name), item['isin'])
            os.makedirs(isin_folder, exist_ok=True)

            # Download PDF and get file path
            file_path = os.path.join(isin_folder, os.path.basename(urlparse(item['download_url']).path))
            response = requests.get(item['download_url'], stream=True)
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)


            md5_hash = hashlib.md5(open(file_path, 'rb').read()).hexdigest()

            csv_writer.writerow([
                item['isin'],
                item['document_type'],
                item['effective_date'],
                item['file_size'],
                file_path,
                item['download_url'],
                datetime.now().strftime('%Y-%m-%d'),
                md5_hash
            ])
        return item

    def check_existing_data(self, csv_file, item):
        # Check by pdf url, this choice can be discussed with domain knowledge
        # Note: Currently using 'download_url' for differentiation, consider other fields
        csv_file.seek(0)
        csv_reader = csv.DictReader(csv_file)
        return any(row['download_url'] == item['download_url'] for row in csv_reader)
