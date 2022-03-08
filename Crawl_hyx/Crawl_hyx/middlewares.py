# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import logging
import time
from telnetlib import EC

import scrapy
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.http import HtmlResponse
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class CrawlHyxDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    # def __init__(self, timeout=25):
    #     chrome_options = Options()
    #     prefs = {
    #         'profile.default_content_setting_values': {
    #             'images': 2,  # 禁用图片的加载
    #             'javascript': 2  # 禁用js，可能会导致通过js加载的互动数抓取失效
    #         }
    #     }
    #     chrome_options.add_experimental_option("prefs", prefs)
    #     self.browser = webdriver.Chrome(executable_path="D:\Python\Crawler_hyx\chromedriver.exe",
    #                                     chrome_options=chrome_options)
    #     self.timeout = timeout
    #     self.browser.maximize_window()
    #     # self.browser.implicitly_wait(20)
    #     # self.browser.set_page_load_timeout(25)
    #     self.browser.set_page_load_timeout(self.timeout)
    #     self.wait = WebDriverWait(self.browser, self.timeout)

    def process_request(self, request, spider):
        # chrome_options = Options()
        # chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('--no-sandbox')
        # # 指定谷歌浏览器路径
        # self.driver = webdriver.Chrome(chrome_options=chrome_options,
        #                                executable_path='D:\Python\Crawler_hyx\chromedriver.exe')
        # self.driver.get(request.url)
        # time.sleep(1)
        # html = self.driver.page_source
        # self.driver.quit()
        # return scrapy.http.HtmlResponse(url=request.url, body=html, encoding='utf-8', request=request)
        return None

    #该方法拦截网易军事板块的对应的响应对象，进行篡改
    def process_response(self, request, response, spider):
        #挑选出指定的响应对象进行篡改
        #通过url指定request
        #通过request指定response
        #实例化一个新的响应对象（包含动态加载的新闻数据），如何获取动态加载的新闻数据
        #基于selenium便捷获取动态加载数据
        bro = spider.bro
        # print('request'+response.url)
        # print(spider.start_urls)
        bro.get(request.url)
        sleep(2)
        page_text = bro.page_source  # 包含了动态加载的新闻
        # print(page_text)
        new_response = HtmlResponse(url=request.url, body=page_text.encode('utf-8'), encoding='utf-8', request=request)
        return new_response
        # if request.url in spider.start_urls:
        #     bro.get(request.url)
        #     sleep(2)
        #     page_text = bro.page_source  #包含了动态加载的新闻
        #     # print(page_text)
        #     new_response = HtmlResponse(url=request.url, body=page_text.encode('utf-8'), encoding='utf-8', request=request)
        #     return new_response
        # else:
        #     return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass


