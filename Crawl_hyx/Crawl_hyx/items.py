# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlHyxItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class WanyiItem(scrapy.Item):
    source = scrapy.Field()  #情报源
    regTime = scrapy.Field()  #情报源注册时长
    followNum = scrapy.Field()  #情报源关注者数目
    title = scrapy.Field()  #文章标题
    fromWhere = scrapy.Field()  #转自何处
    author = scrapy.Field()  #文章作者
    pubTime = scrapy.Field()  #文章发布时间
    timestamp = scrapy.Field()  #爬取时间
    content = scrapy.Field()  #文章正文
    readNum = scrapy.Field()  #阅读数
    retweetNum = scrapy.Field()  #转发数
    url = scrapy.Field()  #链接
    img_url = scrapy.Field() #图片链接

class TengxunItem(scrapy.Item):
    source = scrapy.Field()  #情报源
    regTime = scrapy.Field()  #情报源注册时长
    followNum = scrapy.Field()  #情报源关注者数目
    title = scrapy.Field()  #文章标题
    fromWhere = scrapy.Field()  #转自何处
    author = scrapy.Field()  #文章作者
    pubTime = scrapy.Field()  #文章发布时间
    timestamp = scrapy.Field()  #爬取时间
    content = scrapy.Field()  #文章正文
    readNum = scrapy.Field()  #阅读数
    retweetNum = scrapy.Field()  #转发数
    url = scrapy.Field()  #链接
    img_url = scrapy.Field()  # 图片链接

class BaiduItem(scrapy.Item):
    source = scrapy.Field()  #情报源
    regTime = scrapy.Field()  #情报源注册时长
    followNum = scrapy.Field()  #情报源关注者数目
    title = scrapy.Field()  #文章标题
    fromWhere = scrapy.Field()  #转自何处
    author = scrapy.Field()  #文章作者
    pubTime = scrapy.Field()  #文章发布时间
    timestamp = scrapy.Field()  #爬取时间
    content = scrapy.Field()  #文章正文
    readNum = scrapy.Field()  #阅读数
    retweetNum = scrapy.Field()  #转发数
    url = scrapy.Field()  #链接

class BaidubaikeItem(scrapy.Item):
    source = scrapy.Field()  #情报源
    regTime = scrapy.Field()  #情报源注册时长
    followNum = scrapy.Field()  #情报源关注者数目
    title = scrapy.Field()  #文章标题
    fromWhere = scrapy.Field()  #转自何处
    author = scrapy.Field()  #文章作者
    pubTime = scrapy.Field()  #文章发布时间
    timestamp = scrapy.Field()  #爬取时间
    content = scrapy.Field()  #文章正文
    attributes = scrapy.Field()  #属性
    readNum = scrapy.Field()  #阅读数
    retweetNum = scrapy.Field()  #转发数
    url = scrapy.Field()  #链接

class ImageItem(scrapy.Item):
    image_urls = scrapy.Field()
    title = scrapy.Field()