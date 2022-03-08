import datetime
from time import sleep

import requests
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from ..items import BaiduItem

class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    # allowed_domains = ['www.baidu.com']
    # start_urls = ['https://www.baidu.com//']
    custom_settings = {
        'ITEM_PIPELINES': {'Crawl_hyx.pipelines.BaiduPipeline': 500},
    }

    def __init__(self, *args, **kwargs):
        # self.bro = webdriver.Chrome(executable_path='D:\Python\Crawler_hyx\chromedriver.exe')
        super().__init__(*args, **kwargs)
        self.errback_httpbin = None
        self.keyword = '美国军事'
        self.start_urls = ["https://www.baidu.com/"]
        self.url_list = []
        self.number = -1

        options = webdriver.ChromeOptions()
        prefs = {
            'profile.default_content_setting_values':
                {'notifications': 2,
                 'images': 2}  # 禁止谷歌浏览器弹出通知消息
        }
        options.add_experimental_option('prefs', prefs)
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        # 设置chrome浏览器无界面模式
        # options.add_argument('--headless')
        self.bro = webdriver.Chrome(options=options, executable_path='D:\Python\Crawler_hyx\chromedriver.exe')
        self.bro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                            {'source': 'Object.defineProperty(navigator,"webdriver",{get:()=>undefind})'})
        # browser.maximize_window()  # 浏览器窗口最大化
        self.bro.implicitly_wait(1)  # 隐形等待10秒

    # def start_requests(self):
    #     for u in self.start_urls:
    #         yield scrapy.Request(url = u, callback=self.parse, errback=self.errback_httpbin, dont_filter=True)

    def parse(self, response):
        self.number += 1
        self.bro.get(response.url)
        # 搜索框定位交互
        search_input = self.bro.find_element(By.ID, 'kw')
        search_input.send_keys('美国军事')
        # 点击搜索按钮
        btn = self.bro.find_element(By.XPATH, '//*[@id="su"]')
        btn.click()
        sleep(2)
        zixunurl = self.bro.find_element(By.XPATH, '//*[@id="s_tab"]/div/a[1]')
        zixunurl = zixunurl.get_attribute("href")
        # print(zixunurl)
        self.bro.get(zixunurl)
        # sleep(5)

        # 一页全爬
        div_list = self.bro.find_elements(By.XPATH, '//*[@id="content_left"]/div[2]/div')
        for div in div_list:
            url = div.find_element(By.XPATH, './div/h3/a')
            url = url.get_attribute("href")
            print(url)
            item = BaiduItem()
            item['url'] = url
            #获取页面详情
            # self.bro.get(url)
            # sleep(5)
            type = div.find_element(By.XPATH, './div/div/div/div/span').text
            print('type:'+type)
            item['source'] = type
            # if type == '澎湃新闻':
            #     print('456')
            #     # yield scrapy.Request(url=url, callback=self.parse_pengpai, meta={'item': item})
            # elif type == '新浪军事':
            #     # yield scrapy.Request(url=url, callback=self.parse_xinlang, meta={'item': item})
            #     print('123')
            yield scrapy.Request(url=url, callback=self.parse_url, meta={'item': item})

    def parse_url(self, response):
        print(response.url)
        item = response.meta['item']
        print(item['source'])
        if item['source'] == '澎湃新闻' or item['source'] == '新华网' or item['source'] == '第一财经' or item['source'] == '财联社' or item['source'] == '兵器世界':
            title = response.xpath('//*[@id="ssr-content"]/div[2]/div[1]/div/div[1]//text()').extract_first()
            item['title'] = title
            print(item['title'])
            author = response.xpath('//*[@id="ssr-content"]/div[2]/div[1]/div/div[2]/div[2]/a/p//text()').extract_first()
            item['author'] = author
            pubTime = response.xpath('//*[@id="ssr-content"]/div[2]/div[1]/div/div[2]/div[2]/div/span[1]//text()').extract_first()
            item['pubTime'] = pubTime
            try:
                cont = ''
                contentlist = response.xpath('//*[@id="ssr-content"]/div[2]/div[2]/div[1]/div[1]/div')
                for con in contentlist:
                    cont = cont + con.xpath('./p/span//text()').extract_first()
                if cont:
                    content1 = cont.replace('\n', '')
                    cont = content1.replace('\r', '')
                    content1 = cont.replace(chr(10), ' ')
                    cont = content1.replace('\"', '\'')
                    content = cont.replace('\\', '')
                    item['content'] = content
            except:
                content = ""
                item['content'] = content

            item['timestamp'] = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
            item['regTime'] = ''
            item['followNum'] = ''
            item['fromWhere'] = ''
            item['readNum'] = ''
            item['retweetNum'] = ''
            yield item

        elif item['source'] == '网易':
            title = response.xpath('//*[@id="contain"]/div[1]/h1//text()').extract_first()
            item['title'] = title
            author = response.xpath('//*[@id="contain"]/div[1]/div[2]/a[1]//text()').extract_first()
            item['author'] = author
            pubTime = response.xpath('//*[@id="contain"]/div[1]/div[2]/text()[1]').extract_first()
            item['pubTime'] = pubTime
            content = response.xpath('//*[@id="content"]/div[2]//text()').extract()
            content = ''.join(content)
            item['content'] = content

            followNum = response.xpath('//*[@id="contain"]/div[2]/div[1]/div[4]/span[2]/a/em//text()').extract_first()
            readNum = response.xpath('//*[@id="tieArea"]/div[1]/div/a[2]//text()').extract_first()
            retweetNum = response.xpath('//*[@id="tieArea"]/div[1]/div/a[1]//text()').extract_first()
            item['timestamp'] = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
            item['regTime'] = ''
            item['followNum'] = followNum
            item['fromWhere'] = ''
            item['readNum'] = readNum
            item['retweetNum'] = retweetNum
            yield item

        elif item['source'] == '新浪军事':
            title = response.xpath('/html/body/div[4]/h1//text()').extract_first()
            item['title'] = title
            author = response.xpath('//*[@id="top_bar"]/div/div[2]/a//text()').extract_first()
            item['author'] = author
            pubTime = response.xpath('///*[@id="top_bar"]/div/div[2]/span/text()[1]').extract_first()
            item['pubTime'] = pubTime
            content = response.xpath('//*[@id="article"]//text()').extract()
            content = ''.join(content)
            item['content'] = content

            followNum = ''
            readNum = response.xpath('//*[@id="bottom_sina_comment"]/div[1]/div[1]/span[1]/em[2]/a//text()').extract_first()
            retweetNum = ''
            item['timestamp'] = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
            item['regTime'] = ''
            item['followNum'] = followNum
            item['fromWhere'] = ''
            item['readNum'] = readNum
            item['retweetNum'] = retweetNum
            yield item

        elif item['source'] == '腾讯网':
            title = response.xpath('//*[@id="__xw_next_view_root"]/div/div[3]/div[1]/h1/text()').extract_first()
            item['title'] = title
            author = response.xpath('//*[@id="__xw_next_view_root"]/div/div[3]/div[1]/a[1]/div[2]/div[1]//text()').extract_first()
            item['author'] = author
            pubTime = response.xpath('//*[@id="__xw_next_view_root"]/div/div[3]/div[1]/a[1]/div[2]/div[2]/@title').extract_first()
            item['pubTime'] = pubTime
            content = response.xpath('//*[@id="article_body"]/div[1]//text()').extract()
            content = ''.join(content)
            item['content'] = content

            followNum = ''
            readNum = ''
            retweetNum = ''
            item['timestamp'] = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
            item['regTime'] = ''
            item['followNum'] = followNum
            item['fromWhere'] = ''
            item['readNum'] = readNum
            item['retweetNum'] = retweetNum
            yield item

    def closed(self, spider):
        self.bro.quit()
