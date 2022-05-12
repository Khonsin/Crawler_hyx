"""
user: adm
date: 2021/7/23
time: 15:21
IDE: PyCharm  
"""
import datetime
import json
import logging
import os

import requests
from scrapy import signals
import scrapy
from scrapy.crawler import CrawlerRunner, Crawler
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, error
from threading import Thread
from Crawl_hyx.spiders.baidubaike import BaidubaikeSpider


# logging.basicConfig(level=logging.DEBUG,
#                     format='[%(asctime)-15s] [%(levelname)8s] [%(name)10s ] - %(message)s (%(filename)s:%(lineno)s)',
#                     datefmt='%Y-%m-%d %T'
#                     )
# logger = logging.getLogger(__name__)
WEB_MAP = {"百度百科": 'baidubaike',
           "维基百科": "wiki",
           "百度": "baidu",
           "网易": "wangyi",
           "腾讯": "tengxun"
           }
SITE_to_SPIDER = {"百度百科": BaidubaikeSpider}
NUM = 0

class run_thread(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        start_spiders()

def stop(*args, **kwargs):
    if reactor.running:
        try:
            reactor.stop()
        except error.ReactorNotRunning:
            pass


def start_spiders(info):
    """
    启动爬虫

    :return:
    """

    while True:
        keywords = info['keywords']
        info = {"sites": ['wangyi', 'tengxun', 'wiki', 'baidubaike', 'baidu'], "keywords": keywords}
        if info is not False:
            # logger.info('TextCrawler On!')
            if info is not None:
                sites = info['sites']
                spiders_count = len(keywords) * len(sites)
                configure_logging()
                runner = CrawlerRunner(get_project_settings())
                for keyword in keywords:
                    for site in sites:
                        runner.crawl(site, keyword=keyword, spiders_count=spiders_count)
                        d = runner.join()
                        d.addBoth(stop)

                reactor.run()
            break
        break
    pass




if __name__ == '__main__':
    'TODO:'
    info = {"keywords": "俄乌"}
    start_spiders(info=info)

    