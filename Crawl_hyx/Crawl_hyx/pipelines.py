# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import os
import datetime
import time

import scrapy
from scrapy.pipelines.images import ImagesPipeline

from itemadapter import ItemAdapter
SavePath = 'result'
def CreatePath(path, tag):
    """
    判断保存路径是否存在，如果不存在则创建
    :param tag:
    :param path:
    :return:
    """
    path = path + '/{}/'.format(tag)
    if os.path.exists(path) is False:
        os.makedirs(path)
    SaveFile = path + '{}_'.format(tag) + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f") + '.json'
    if os.path.exists(SaveFile) is False:
        file = open(SaveFile, "a+", newline="", encoding="utf-8-sig")
    else:
        file = open(SaveFile, "a+", newline="", encoding="utf-8-sig")
    return file

def create_count_file(path, tag, keyword):
    index_path = path + '/count'
    if os.path.exists(index_path) is False:
        os.makedirs((index_path))
    count_file = index_path + '/{}_{}_{}'.format(str(datetime.datetime.now().strftime("%Y%m%d%H%M%S")), tag, keyword)
    try:
        return open(count_file, 'w', encoding='utf-8')
    except:
        time.sleep(1)
        return open(count_file, 'w', encoding='utf-8')

class CrawlHyxPipeline:
    def process_item(self, item, spider):
        return item

class WanyiPipeline:
    def __init__(self):
        self.tag = 'wanyi'
        self.file = CreatePath(SavePath, self.tag)
        self.data = []
        self.count = 0
        self.first = True

    def process_item(self, item, spider):
        if self.first:
            # self.count_file = create_count_file(SavePath, self.tag, item["keyword"])
            self.first = False
        detail_ = {"情报源": item["source"], "情报源注册时长": item["regTime"], "情报源关注者数目": item["followNum"], "文章标题": item["title"],
                   "转自何处": item["fromWhere"], "文章作者": item["author"], "文章发布时间": item["pubTime"], "爬取时间": item["timestamp"],
                   "文章正文": item["content"], "阅读数": item["readNum"], "转发数": item["retweetNum"], "链接": item["url"]}
        self.data.append(detail_)
        self.count += 1
        return item


    def close_spider(self, spider):
        json.dump(self.data, self.file, indent=4, ensure_ascii=False)
        self.file.close()
        if self.first is False:
            self.file.write(str(self.count))
            self.file.close()

class TengxunPipeline:
    def __init__(self):
        self.tag = 'tengxun'
        self.file = CreatePath(SavePath, self.tag)
        self.data = []
        self.count = 0
        self.first = True

    def process_item(self, item, spider):
        if self.first:
            # self.count_file = create_count_file(SavePath, self.tag, item["keyword"])
            self.first = False
        detail_ = {"情报源": item["source"], "情报源注册时长": item["regTime"], "情报源关注者数目": item["followNum"], "文章标题": item["title"],
                   "转自何处": item["fromWhere"], "文章作者": item["author"], "文章发布时间": item["pubTime"], "爬取时间": item["timestamp"],
                   "文章正文": item["content"], "阅读数": item["readNum"], "转发数": item["retweetNum"], "链接": item["url"]}
        self.data.append(detail_)
        self.count += 1
        return item


    def close_spider(self, spider):
        json.dump(self.data, self.file, indent=4, ensure_ascii=False)
        self.file.close()
        if self.first is False:
            self.file.write(str(self.count))
            self.file.close()

class BaiduPipeline:
    def __init__(self):
        self.tag = 'baidu'
        self.file = CreatePath(SavePath, self.tag)
        self.data = []
        self.count = 0
        self.first = True

    def process_item(self, item, spider):
        if self.first:
            # self.count_file = create_count_file(SavePath, self.tag, item["keyword"])
            self.first = False
        detail_ = {"情报源": item["source"], "情报源注册时长": item["regTime"], "情报源关注者数目": item["followNum"], "文章标题": item["title"],
                   "转自何处": item["fromWhere"], "文章作者": item["author"], "文章发布时间": item["pubTime"], "爬取时间": item["timestamp"],
                   "文章正文": item["content"], "阅读数": item["readNum"], "转发数": item["retweetNum"], "链接": item["url"]}
        self.data.append(detail_)
        self.count += 1
        return item


    def close_spider(self, spider):
        json.dump(self.data, self.file, indent=4, ensure_ascii=False)
        self.file.close()
        if self.first is False:
            self.file.write(str(self.count))
            self.file.close()

class BaidubaikePipeline:
    def __init__(self):
        self.tag = 'baidubaike'
        self.file = CreatePath(SavePath, self.tag)
        self.data = []
        self.count = 0
        self.first = True

    def process_item(self, item, spider):
        if self.first:
            # self.count_file = create_count_file(SavePath, self.tag, item["keyword"])
            self.first = False
        detail_ = {"情报源": item["source"], "情报源注册时长": item["regTime"], "情报源关注者数目": item["followNum"], "文章标题": item["title"],
                   "转自何处": item["fromWhere"], "文章作者": item["author"], "文章发布时间": item["pubTime"], "爬取时间": item["timestamp"],
                   "文章正文": item["content"], "属性": item['attributes'], "阅读数": item["readNum"], "转发数": item["retweetNum"], "链接": item["url"]}
        self.data.append(detail_)
        self.count += 1
        return item


    def close_spider(self, spider):
        json.dump(self.data, self.file, indent=4, ensure_ascii=False)
        self.file.close()
        if self.first is False:
            self.file.write(str(self.count))
            self.file.close()


class ImagePipeline(ImagesPipeline):
    #图片地址请求
    def get_media_requests(self, item, info):
        # print(item['img_url'])
        for url in item['img_url']:
            # print(url)
            yield scrapy.Request(url)

    # 保存图片时重命名
    def item_completed(self, results, item, info):
        # print(results)
        # print("*"* 30)
        # 列表推导式，获取图片的保存路径
        image_url = [x["path"] for ok, x in results if ok]
        print(image_url[0])

        # 重命名，由于都是jpg文件，所以直接拼上了
        os.rename(SavePath+image_url[0], SavePath + item["title"] + ".jpg")
        return item