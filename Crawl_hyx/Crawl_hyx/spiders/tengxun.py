import datetime
import os
import time

import scrapy
from selenium import webdriver
from ..items import TengxunItem
import requests
from selenium.webdriver.common.by import By

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
}

class TengxunSpider(scrapy.Spider):
    name = 'tengxun'
    # allowed_domains = ['new.qq.com/ch/milite/']
    # start_urls = ['https://new.qq.com/ch/milite/']
    custom_settings = {
        'ITEM_PIPELINES': {'Crawl_hyx.pipelines.TengxunPipeline': 300,
                            'Crawl_hyx.pipelines.ImagePipeline': 300},
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
            for r in range(15):
                time.sleep(1)
                self.bro.execute_script("window.scrollBy(0,2000)")
            check_height1 = self.bro.execute_script("return document.body.scrollHeight;")
            end1 = time.time()
            if check_height == check_height1:
                t = False
                print('t:'+t)

        time.sleep(1)
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

        # 获取图片
        cnt = 0
        image = 'image'
        if not os.path.exists(image):
            os.mkdir(image)
        image_urls = response.xpath('/html/body/div[3]/div[1]/div[1]/div[2]/p/img/@src').extract()
        # print(image_urls)
        for image_url in image_urls:
            # image_url = image_url.xpath('./img/@src').extract_first()
            cnt = cnt + 1
            # img_url["图片" + str(cnt)] = str(image_url)
            # time.sleep(2)
            # 下载数据:
            image_url = 'https:' + image_url
            # print(image_url)
            res = requests.get(image_url, headers=headers)
            data = res.content
            try:
                with open(image + '/tengxun/' + title + '(' + str(cnt) + ').jpg', 'wb') as f:
                    f.write(data)
                    print('%s下载成功' % title)
                    f.close()
            except:
                break
        # print(img_url)
        item['img_url'] = image_urls

        # result = 'video'
        # if not os.path.exists(result):
        #     os.mkdir(result)
        # video_urls = response.xpath('//*[@id="content"]/div[2]/p/video/@src').extract()
        # for video_url in video_urls:
        #     # 下载数据:
        #     res = requests.get(video_url, headers=headers)
        #     data = res.content
        #     try:
        #         with open(result + '/tengxun/' + title + '.mp4', 'wb') as f:
        #             f.write(data)
        #             print('%s下载成功' % title)
        #             f.close()
        #     except:
        #         break
        yield item

    def closed(self, spider):
        self.bro.quit()
