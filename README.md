#### Setup
1. Clone repository
2. Navigate to the project directory:

    cd  /path/to/your/scrapy/project


#### Project structure:
```bash
fund_project/
│
├── fund_project/
│   ├── __init__.py
│   ├── items.py
│   ├── pipelines.py
│   ├── settings.py
│   └── spiders/
│       ├── __init__.py
│       └── fund_spider.py  
│
├── run.py
├── requirements.txt
├── FundDatabase/..  
│
└── scrapy.cfg
```

#### Install requirements:
pip install -r requirements.txt


#### Run schedule(unix based):
Open the terminal and run cron scheduler: crontab -e.  
Add a new line with the following format:  
```bash
0 0 * * /path/to/python3 /path/to/run.py
```

(on Windows use Task scheduler)  
(To run the spider manually: scrapy crawl fund)


