import datetime
import time

import scrapy
from selenium import webdriver
from ..items import BaidubaikeItem

class BaidubaikeSpider(scrapy.Spider):
    name = 'baidubaike'
    # allowed_domains = ['www.baike.baidu.com']
    # start_urls = ['http://www.baike.baidu.com/']
    custom_settings = {
        'ITEM_PIPELINES': {'Crawl_hyx.pipelines.BaidubaikePipeline': 400},
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.allowed_domains = ['www.baike.baidu.com']
        self.keyword = '美国军事'
        self.start_urls = ["https://baike.baidu.com/item/" + self.keyword]
        self.number = -1

        options = webdriver.ChromeOptions()
        prefs = {
            'profile.default_content_setting_values':
                {'notifications': 2,
                 'images': 2}  # 禁止谷歌浏览器弹出通知消息
        }
        options.add_experimental_option('prefs', prefs)
        # 设置chrome浏览器无界面模式
        options.add_argument('--headless')
        self.bro = webdriver.Chrome(options=options, executable_path='D:\Python\Crawler_hyx\chromedriver.exe')
        # browser.maximize_window()  # 浏览器窗口最大化
        self.bro.implicitly_wait(1)  # 隐形等待10秒

    def parse(self, response):
        self.number += 1
        # self.keyword = self.keywords[self.number]
        name = response.xpath("/html/body/div[3]/div[2]/div/div[1]/dl[1]/dd/span/h1/text()").extract_first()
        item = BaidubaikeItem()

        # 简介
        try:
            cont = ""
            content1 = response.xpath("/html/body/div[3]/div[2]/div/div/div[4]//text()").extract()
            for con in content1:
                cont = cont + con
            if cont:
                content1 = cont.replace('\n', '')
                cont = content1.replace('\r', '')
                content1 = cont.replace(chr(10), ' ')
                cont = content1.replace('\"', '\'')
                content = cont.replace('\\', '')
            else:
                return item
        except:
            content = ""

        # 属性
        attr = dict()
        attr_names = response.xpath("//dt[@class='basicInfo-item name']//text()").extract()
        attr_values = response.xpath("//dd[@class='basicInfo-item value']//text()").extract()
        for i, attr_n in enumerate(attr_names):
            attr_n = attr_n.replace(' ', '')
            attr_n = attr_n.replace(chr(10), '')
            attr_n = attr_n.replace('\"', '\'')
            attr_names[i] = "".join(str(attr_n).split())
            attr_values[i] = attr_values[i].replace(chr(10), '')
            attr_values[i] = attr_values[i].replace('\\xa0', '')
            attr_values[i] = attr_values[i].replace('\"', '\'')
            # attr = attr + ", \"" + str(attr_names[i]) + "\" : \"" + str(attr_values[i]) + "\""
            attr[str(attr_names[i])] = str(attr_values[i])

        # 加载所有图片
        cnt = 0
        # 设置浏览器
        self.bro.get(response.url)

        # 下拉滑动条至底部，加载出所有帖子信息
        t = True
        start = time.time()
        end1 = time.time()
        while t and (end1 - start) < 5:
            check_height = self.bro.execute_script("return document.body.scrollHeight;")
            for r in range(4):
                time.sleep(2)
                self.bro.execute_script("window.scrollBy(0,1500)")
            check_height1 = self.bro.execute_script("return document.body.scrollHeight;")
            end1 = time.time()
            if check_height == check_height1:
                t = False

        item['source'] = '百度百科'
        item['regTime'] = ''
        item['followNum'] = ''
        item['title'] = str(name)
        item['fromWhere'] = ''
        item['author'] = ''
        item['pubTime'] = ''
        item['timestamp'] = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        item['content'] = str(content)
        item['attributes'] = attr
        item['url'] = response.url
        item['readNum'] = ''
        item['retweetNum'] = ''
        if len(item['content'].replace(' ', '').replace("\n", '')) <= 20 or item['content'] == '':
            return
        yield item

    def closed(self, spider):
        self.bro.quit()