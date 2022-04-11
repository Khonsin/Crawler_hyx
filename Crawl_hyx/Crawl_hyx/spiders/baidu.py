import datetime
import random
import time
from time import sleep

import requests
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from ..items import BaiduItem
from ..settings import USER_AGENT_LIST
from webdriver_manager.chrome import ChromeDriverManager

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
        self.keyword = '俄乌'
        # if 'keyword' in kwargs:
        #     self.keyword = kwargs['keyword']
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
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        # self.bro = webdriver.Chrome(options=options, executable_path='D:\Python\Crawler_hyx\chromedriver.exe')
        self.bro = webdriver.Chrome(ChromeDriverManager().install())
        self.bro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                            {'source': 'Object.defineProperty(navigator,"webdriver",{get:()=>undefind})'})
        # browser.maximize_window()  # 浏览器窗口最大化
        self.bro.implicitly_wait(1)  # 隐形等待10秒

    # def start_requests(self):
    #     for u in self.start_urls:
    #         yield scrapy.Request(url = u, callback=self.parse, errback=self.errback_httpbin, dont_filter=True)

    def get_proxy(self):
        # 5000：settings中设置的监听端口，不是Redis服务的端口
        return requests.get("http://127.0.0.1:5010/get/").json()

    def parse(self, response):
        self.number += 1
        self.bro.get(response.url)
        # 搜索框定位交互
        search_input = self.bro.find_element(By.ID, 'kw')
        search_input.send_keys(self.keyword)  # self.keyword
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
        div_list = self.bro.find_elements(By.XPATH, '//*[@id="content_left"]/div')
        for div in div_list[1:]:
            url = div.find_element(By.XPATH, "./div/h3/a")
            url = url.get_attribute("href")
            # print(url)
            item = BaiduItem()
            item['url'] = url
            # 获取页面详情
            # self.bro.get(url)
            # sleep(5)
            type1 = div.find_element(By.XPATH, './div/div/div/div/a[1]/span').text
            # print('type:'+type1)
            item['source'] = type1

            time.sleep(2)
            ua = random.choice(USER_AGENT_LIST)
            headers = {'User-Agent': ua,
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
            print(url)
            proxy = self.get_proxy().get("proxy")
            yield scrapy.Request(url=url, callback=self.parse_url, meta={'item': item}, headers=headers)

    def parse_url(self, response):
        print(response.url)
        item = response.meta['item']
        # print(item['source'])

        if item['source'] == '网易':
            title = response.xpath('//*[@id="contain"]/div[1]/h1//text()').extract_first()
            item['title'] = title
            author = response.xpath('//*[@id="contain"]/div[1]/div[2]/a[1]//text()').extract_first()
            item['author'] = author
            pubTime = response.xpath('//*[@id="contain"]/div[1]/div[2]/text()[1]').extract_first()
            item['pubTime'] = pubTime
            content = response.xpath('//*[@id="content"]/div[2]//text()').extract()
            content = ''.join(content)
            if content:
                content = content.replace('\n', '').replace('\r', '').replace(chr(10), ' ').replace('\"', '\'').replace('\\', '')
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
            if content:
                content = content.replace('\n', '').replace('\r', '').replace(chr(10), ' ').replace('\"', '\'').replace('\\', '')
            item['content'] = content

            readNum = response.xpath('//*[@id="bottom_sina_comment"]/div[1]/div[1]/span[1]/em[2]/a//text()').extract_first()
            item['timestamp'] = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
            item['regTime'] = ''
            item['followNum'] = ''
            item['fromWhere'] = ''
            item['readNum'] = readNum
            item['retweetNum'] = ''
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
            if content:
                content = content.replace('\n', '').replace('\r', '').replace(chr(10), ' ').replace('\"', '\'').replace('\\', '')
            item['content'] = content

            item['timestamp'] = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
            item['regTime'] = ''
            item['followNum'] = ''
            item['fromWhere'] = ''
            item['readNum'] = ''
            item['retweetNum'] = ''
            yield item

        elif item['source'] == '新华网客户端':
            title = response.xpath('/html/body/div[3]/div[3]/div[1]/h1/text()').extract_first()
            item['title'] = title
            author = response.xpath('//*[@id="articleEdit"]/span[2]//text()').extract_first()
            if author:
                author = author.replace('\n', '')
            item['author'] = author
            pubTime = response.xpath('/html/body/div[3]/div[2]/div[1]//text()').extract_first()
            # pubTime = ''.join(pubTime)
            # pubTime1 = response.xpath('/html/body/div[4]/div[2]/div[1]//text()').extract()
            # if pubTime != []:
            #     item['pubTime'] = pubTime.replace('\n', '')
            # elif pubTime1 != []:
            #     item['pubTime'] = pubTime1
            item['pubTime'] = pubTime.replace('\n', '')
            content = response.xpath('//*[@id="detail"]//text()').extract()
            content = ''.join(content)
            if content:
                content = content.replace('\n', '').replace('\r', '').replace(chr(10), ' ').replace('\"', '\'').replace('\\', '')
            item['content'] = content

            fromWhere = response.xpath('/html/body/div[3]/div[2]/div[3]//text()').extract_first()
            item['timestamp'] = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
            item['regTime'] = ''
            item['followNum'] = ''
            item['fromWhere'] = fromWhere
            item['readNum'] = ''
            item['retweetNum'] = ''
            yield item

        elif item['source'] == '央广网':
            title = response.xpath('//*[@id="main"]/div[2]/div[1]/h1/text()').extract_first()
            item['title'] = title
            author = response.xpath('//*[@id="main"]/div[2]/div[2]/div[2]/div[2]/span/text()').extract_first()
            item['author'] = author
            pubTime = response.xpath('//*[@id="main"]/div[2]/div[1]/div/span[1]//text()').extract_first()
            item['pubTime'] = pubTime
            content = response.xpath('//*[@id="main"]/div[2]/div[2]/div[2]/div[1]//text()').extract()
            content = ''.join(content)
            if content:
                content = content.replace('\n', '').replace('\r', '').replace(chr(10), ' ').replace('\"', '\'').replace('\\', '').replace('\t', '')
            item['content'] = content

            fromWhere = response.xpath('//*[@id="main"]/div[2]/div[1]/div/span[2]//text()').extract_first()
            item['timestamp'] = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
            item['regTime'] = ''
            item['followNum'] = ''
            item['fromWhere'] = fromWhere
            item['readNum'] = ''
            item['retweetNum'] = ''
            yield item

        elif item['source'] == '光明网':
            title = response.xpath('//*[@id="title"]/text()').extract_first()
            item['title'] = title
            author = '光明网'
            item['author'] = author
            pubTime = response.xpath('//*[@id="container"]/div/div[2]/span/text()').extract_first()
            item['pubTime'] = pubTime
            content = response.xpath('//*[@id="container"]/article//text()').extract()
            content = ''.join(content)
            if content:
                content = content.replace('\n', '').replace('\r', '').replace(chr(10), ' ').replace('\"', '\'').replace('\\', '')
            item['content'] = content

            item['timestamp'] = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
            item['regTime'] = ''
            item['followNum'] = ''
            item['fromWhere'] = ''
            item['readNum'] = ''
            item['retweetNum'] = ''
            yield item

        # elif item['source'] == '国际在线':
        #     title = response.xpath('/html/body/article/div/h1/text()').extract_first()
        #     item['title'] = title
        #     author = response.xpath('/html/body/article/div/div[1]/span[1]/text()').extract_first()
        #     item['author'] = author
        #     pubTime = response.xpath('/html/body/article/div/div[1]/span[2]/text()').extract_first()
        #     item['pubTime'] = pubTime
        #     content = response.xpath('/html/body/article/div/div[2]//text()').extract()
        #     content = ''.join(content)
        #     if content:
        #         content = content.replace('\n', '').replace('\r', '').replace(chr(10), ' ').replace('\"', '\'').replace('\\', '')
        #     item['content'] = content
        #
        #     item['timestamp'] = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        #     item['regTime'] = ''
        #     item['followNum'] = ''
        #     item['fromWhere'] = ''
        #     item['readNum'] = ''
        #     item['retweetNum'] = ''
        #     yield item

        elif item['source'] == '央视网':
            title = response.xpath('//*[@id="title_area"]/h1/text()').extract_first()
            item['title'] = title
            author = response.xpath('//*[@id="text_area"]/div//text()').extract()
            item['author'] = author
            pubTime = response.xpath('//*[@id="title_area"]/div/span').extract_first()
            item['pubTime'] = pubTime
            content = response.xpath('//*[@id="text_area"]//text()').extract()
            content = ''.join(content)
            if content:
                content = content.replace('\n', '').replace('\r', '').replace(chr(10), ' ').replace('\"', '\'').replace('\\', '')
            item['content'] = content

            item['timestamp'] = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
            item['regTime'] = ''
            item['followNum'] = ''
            item['fromWhere'] = ''
            item['readNum'] = ''
            item['retweetNum'] = ''
            yield item

        elif item['source'] == '中国网':
            title = response.xpath('/html/body/div[2]/h1/text()').extract_first()
            item['title'] = title
            author = response.xpath('//*[@id="author_baidu"]/text()').extract_first()
            item['author'] = author
            pubTime = response.xpath('//*[@id="pubtime_baidu"]/text()').extract_first()
            item['pubTime'] = pubTime
            content = response.xpath('//*[@id="articleBody"]//text()').extract()
            content = ''.join(content)
            if content:
                content = content.replace('\n', '').replace('\r', '').replace(chr(10), ' ').replace('\"', '\'').replace('\\', '')
            item['content'] = content

            fromWhere = response.xpath('//*[@id="source_baidu"]/a/text()').extract_first()
            item['timestamp'] = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
            item['regTime'] = ''
            item['followNum'] = ''
            item['fromWhere'] = fromWhere
            item['readNum'] = ''
            item['retweetNum'] = ''
            yield item

        elif item['source'] == '上观新闻':
            title = response.xpath('//*[@id="title"]/text()').extract_first()
            item['title'] = title
            author = '上观新闻'
            item['author'] = author
            pubTime = response.xpath('//*[@id="container"]/div/div[2]/span/text()').extract_first()
            item['pubTime'] = pubTime
            content = response.xpath('//*[@id="container"]/article//text()').extract()
            content = ''.join(content)
            if content:
                content = content.replace('\n', '').replace('\r', '').replace(chr(10), ' ').replace('\"', '\'').replace('\\', '')
            item['content'] = content

            item['timestamp'] = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
            item['regTime'] = ''
            item['followNum'] = ''
            item['fromWhere'] = ''
            item['readNum'] = ''
            item['retweetNum'] = ''
            yield item

        elif item['source'] == '澎湃新闻客户端':
            title = response.xpath('//*[@id="title"]/text()').extract_first()
            item['title'] = title
            author = '澎湃新闻'
            item['author'] = author
            pubTime = response.xpath('//*[@id="container"]/div/div[2]/span/text()').extract_first()
            item['pubTime'] = pubTime
            content = response.xpath('//*[@id="container"]/article//text()').extract()
            content = ''.join(content)
            if content:
                content = content.replace('\n', '').replace('\r', '').replace(chr(10), ' ').replace('\"', '\'').replace('\\', '')
            item['content'] = content

            item['timestamp'] = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
            item['regTime'] = ''
            item['followNum'] = ''
            item['fromWhere'] = ''
            item['readNum'] = ''
            item['retweetNum'] = ''
            yield item

        else: # item['source'] == '澎湃新闻' or item['source'] == '新华网' or item['source'] == '第一财经' or item['source'] == '财联社' or item['source'] == '兵器世界' or item['source'] == '海外网' or item['source'] == '潇湘晨报' or item['source'] == '九派新闻' or item['source'] == '排头国际视野' or item['source'] == '经济观察报' or item['source'] == '东方之星V':
            title = response.xpath('//*[@id="ssr-content"]/div[2]/div/div[1]/div[1]/div/div[1]/text()').extract_first()
            item['title'] = title
            print("title:"+item['title'])
            author = response.xpath('//*[@id="ssr-content"]/div[2]/div/div[1]/div[1]/div/div[2]/div[2]/a/p/text()').extract_first()
            item['author'] = author
            pubTime = response.xpath('//*[@id="ssr-content"]/div[2]/div/div[1]/div[1]/div/div[2]/div[2]/div/span[1]/text()').extract_first()
            item['pubTime'] = pubTime
            content = response.xpath('//*[@id="ssr-content"]/div[2]/div/div[1]/div[2]/div[1]//text()').extract()
            content = ''.join(content)
            if content:
                content = content.replace('\n', '').replace('\r', '').replace(chr(10), ' ').replace('\"', '\'').replace(
                    '\\', '')
            item['content'] = content
            # try:
            #     cont = ''
            #     contentlist = response.xpath('//*[@id="ssr-content"]/div[2]/div/div[1]/div[2]/div[1]/div')
            #     for con in contentlist:
            #         cont = cont + con.xpath('./p/span//text()').extract_first()
            #     if cont:
            #         content1 = cont.replace('\n', '')
            #         cont = content1.replace('\r', '')
            #         content1 = cont.replace(chr(10), ' ')
            #         cont = content1.replace('\"', '\'')
            #         content = cont.replace('\\', '')
            #         item['content'] = content
            # except:
            #     content = ""
            #     item['content'] = content

            item['timestamp'] = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
            item['regTime'] = ''
            item['followNum'] = ''
            item['fromWhere'] = ''
            item['readNum'] = ''
            item['retweetNum'] = ''
            yield item

    def closed(self, spider):
        self.bro.quit()
