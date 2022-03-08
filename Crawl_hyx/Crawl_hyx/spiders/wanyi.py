import datetime
import time
from xml import etree

import scrapy
from ..items import WanyiItem
from selenium import webdriver
import requests

class WanyiSpider(scrapy.Spider):
    name = 'wanyi'
    # allowed_domains = ['war.163.com']
    # start_urls = ['http://war.163.com/']
    # url_list = []
    custom_settings = {
        'ITEM_PIPELINES': {'Crawl_hyx.pipelines.WanyiPipeline': 300},
    }

    #实例化一个浏览器对象
    def __init__(self):
        # self.bro = webdriver.Chrome(executable_path='D:\Python\Crawler_hyx\chromedriver.exe')
        # self.bro = webdriver.Chrome(r'D:\Python\Crawler_hyx\chromedriver.exe')
        self.start_urls = ['http://war.163.com/']
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # 使用无头谷歌浏览器模式
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        # 设置chrome浏览器无界面模式
        options.add_argument('--headless')
        self.bro = webdriver.Chrome(options=options,executable_path='D:\Python\Crawler_hyx\chromedriver.exe')
        # browser.maximize_window()  # 浏览器窗口最大化
        self.bro.implicitly_wait(1)  # 隐形等待10秒

    #动态加载的内容
    def parse(self, response):
        # 设置浏览器
        self.bro.get(response.url)
        start = time.time()
        end1 = time.time()
        # 下拉滑动条至底部，加载出所有帖子信息
        t = True
        while t and (end1 - start) < 5:
            check_height = self.bro.execute_script("return document.body.scrollHeight;")
            for r in range(6):
                time.sleep(2)
                self.bro.execute_script("window.scrollBy(0,1000)")
            check_height1 = self.bro.execute_script("return document.body.scrollHeight;")
            end1 = time.time()
            if check_height == check_height1:
                t = False

        # js = 'return document.body.scrollHeight;'
        # height = 0
        # while True:
        #     new_height = self.bro.execute_script(js)
        #     if new_height > height:
        #         self.bro.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        #         height = new_height
        #         time.sleep(5)
        #     else:
        #         print("滚动条已经处于页面最下方!")
        #         self.bro.execute_script('window.scrollTo(0, 0)')  # 页面滚动到顶部
        #         break

        div_list = response.xpath('//div[@class="hidden"]/div')
        # div_list = requests.get(response.url).xpath("/html/body/div/div[3]/div[4]/div[1]/div[1]/div/ul/li/div/div")
        # print(div_list)
        for div in div_list:
            # div = etree.fromstring(div)
            url = div.xpath('./a/@href').extract_first()
            # self.url_list.append(url)
            print(url)
            #对url的详情页发起请求
            yield scrapy.Request(url=url, callback=self.parse_detail)

    #解析新闻内容
    def parse_detail(self, response):
        title = response.xpath('//*[@id="contain"]/div[1]/h1//text()').extract_first()
        # content = response.xpath('//*[@id="content"]/div[2]//text()').extract()
        # content = ''.join(content)
        try:
            cont = ""
            content1 = response.xpath('//*[@id="content"]/div[2]//text()').extract()
            cont = ''.join(content1)
            if cont:
                content1 = cont.replace('\n', '')
                cont = content1.replace('\r', '')
                content1 = cont.replace(chr(10), ' ')
                cont = content1.replace('\"', '\'')
                content = cont.replace('\\', '')
        except:
            content = ""
        followNum = response.xpath('//*[@id="contain"]/div[2]/div[1]/div[4]/span[2]/a/em//text()').extract_first()
        author = response.xpath('//*[@id="contain"]/div[1]/div[2]/a[1]//text()').extract_first()
        pubTime = response.xpath('//*[@id="contain"]/div[1]/div[2]//text()').extract_first()
        readNum = response.xpath('//*[@id="tieArea"]/div[1]/div/a[2]//text()').extract_first()
        retweetNum = response.xpath('//*[@id="tieArea"]/div[1]/div/a[1]//text()').extract_first()
        url = response.xpath('//*[@id="ne_wrap"]/head/link[5]/@href').extract_first()
        # print(response.text)
        item = WanyiItem()
        item['source'] = '网易军事'
        item['regTime'] = ''
        item['title'] = title
        item['followNum'] = followNum
        item['fromWhere'] = ''
        item['author'] = author
        item['pubTime'] = pubTime
        item['timestamp'] = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        item['content'] = content
        item['readNum'] = readNum
        item['retweetNum'] = retweetNum
        item['url'] = url
        #
        yield item

    def closed(self, spider):
        self.bro.quit()