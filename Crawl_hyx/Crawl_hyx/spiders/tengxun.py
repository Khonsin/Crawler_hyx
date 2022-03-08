import datetime
import time

import scrapy
from selenium import webdriver
from ..items import TengxunItem
from selenium.webdriver.common.by import By

class TengxunSpider(scrapy.Spider):
    name = 'tengxun'
    # allowed_domains = ['new.qq.com/ch/milite/']
    # start_urls = ['https://new.qq.com/ch/milite/']
    custom_settings = {
        'ITEM_PIPELINES': {'Crawl_hyx.pipelines.TengxunPipeline': 400},
    }

    # 实例化一个浏览器对象
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = ['https://new.qq.com/ch/milite/']
        options = webdriver.ChromeOptions()
        # 设置chrome浏览器无界面模式
        options.add_argument('--headless')  # 使用无头谷歌浏览器模式
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        self.bro = webdriver.Chrome(options=options, executable_path='D:\Python\Crawler_hyx\chromedriver.exe')
        # browser.maximize_window()  # 浏览器窗口最大化
        self.bro.implicitly_wait(1)  # 隐形等待10秒
        self.url_list = []

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
                print('t:'+t)

        # print(response.text)
        li_list = response.xpath('//*[@id="hot_scroll"]/li')
        for li in li_list:
            # div = etree.fromstring(div)
            url = li.xpath('./a/@href').extract_first()
            if url != None:
                item = TengxunItem()
                author = li.xpath('./div/div[2]/div[1]/a//text()').extract_first()
                print(url)
                print(author)
            # c_time = li.xpath('./div/div[2]/div[1]/span//text()').extract_first()

            # d = 20
            # pubTime = ((datetime.datetime.now()-datetime.timedelta(minutes=c_time)).strftime("%Y-%m-%d %H:%M:%S"))
                item['author'] = author
            # item['pubTime'] = pubTime
                item['url'] = url
            #对url的详情页发起请求
                yield scrapy.Request(url=url, callback=self.parse_detail, meta={'item': item})

    # 解析新闻内容
    def parse_detail(self, response):
        item = response.meta['item']
        # print(item['url'])
        self.bro.get(response.url)
        self.bro.implicitly_wait(10)  # seconds
        title = response.xpath('/html/body/div[3]/div[1]/h1//text()').extract_first()
        # content = response.xpath('/html/body/div[3]/div[1]/div[1]/div[2]//text()').extract()
        # content = ''.join(content)
        try:
            cont = ""
            content1 = response.xpath('/html/body/div[3]/div[1]/div[1]/div[2]//text()').extract()
            cont = ''.join(content1)
            if cont:
                content1 = cont.replace('\n', '')
                cont = content1.replace('\r', '')
                content1 = cont.replace(chr(10), ' ')
                cont = content1.replace('\"', '\'')
                content = cont.replace('\\', '')
                content = content.replace(' ', '')
        except:
            content = ""

        year = response.xpath('//*[@id="LeftTool"]/div/div[1]/span//text()').extract_first()
        date = response.xpath('//*[@id="LeftTool"]/div/div[2]//text()').extract()
        date = ''.join(date)
        time = response.xpath('//*[@id="LeftTool"]/div/div[3]//text()').extract()
        time = ''.join(time)
        pubTime = year + '/' + date + ' ' + time
        # print(pubTime)
        item['source'] = '腾讯军事'
        item['regTime'] = ''
        item['title'] = title
        item['followNum'] = ''
        item['fromWhere'] = ''
        item['timestamp'] = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        item['content'] = content
        item['pubTime'] = pubTime
        item['readNum'] = ''
        item['retweetNum'] = ''
        yield item

    def closed(self, spider):
        self.bro.quit()
