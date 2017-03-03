# coding:utf8
import random
import time
import uuid

from PIL import Image

import config

import url_manager, html_downloader, html_parser, html_outputer


class SpiderMain(object):
    def __init__(self):
        self.db = None
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parse = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def start(self, count, index):
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print 'craw %d : %s' % (count, new_url['href'],)
                html_cont = self.downloader.downloader(new_url['href'])
                new_data = self.parse.article_parse(html_cont)
                if new_data is None: continue
                thumbnail_uuid = str(uuid.uuid1())
                file_name_base = (config.FILESTORAGEPATH % (
                    time.strftime('%Y', time.localtime(time.time())),
                    time.strftime('%m', time.localtime(time.time())),)) + thumbnail_uuid;
                file_name = file_name_base + '.jpeg'
                file_name_150 = file_name_base + '-150x150.jpeg'
                file_name_300 = file_name_base + '-300x169.jpeg'
                if new_url['src']:
                    src = new_url['src']
                    thumbnail = self.downloader.downloader_pic(src, file_name)
                    sImg = Image.open(thumbnail)
                    w, h = sImg.size
                    print w, h
                    t_150, t_300 = 150.0 / w, 300.0 / w
                    print t_150, t_300
                    print int(h * t_150), int(h * t_300)
                    dImg = sImg.resize((150, int(h * t_150)), Image.ANTIALIAS)  # 设置压缩尺寸和选项，注意尺寸要用括号
                    dImg.save(file_name_150)
                    sImg = Image.open(thumbnail)
                    dImg = sImg.resize((300, int(h * t_300)), Image.ANTIALIAS)  # 设置压缩尺寸和选项，注意尺寸要用括号
                    dImg.save(file_name_300)
                else:
                    thumbnail_uuid = None
                self.outputer.collect_data(new_data, thumbnail_uuid, index + 1)
                count = count + 1
                sleep = int(random.random() * 5)
                print 'sleep in %s' % sleep
                time.sleep(sleep)
            except Exception, e:
                print Exception, ":", e
                print 'craw failed'

    def craw(self):
        count = 1
        category_total = 20
        for index in reversed(range(category_total)):
            # 收集本栏目的全部url
            collectors = self.urls.url_collector(index)
            for collector in collectors:
                urls_cont = self.downloader.downloader(collector)
                urls = self.parse.url_parse(urls_cont)
                self.urls.add_new_urls(urls)
                self.start(count, index)
            print 'category ' + str(index) + ' finish'

    def specified(self, index):
        count = 1
        collectors = self.urls.url_collector(index)
        for collector in collectors:
            urls_cont = self.downloader.downloader(collector)
            urls = self.parse.url_parse(urls_cont)
            self.urls.add_new_urls(urls)
            self.start(count, index)
        print 'category ' + str(index) + ' finish'


if __name__ == "__main__":
    import sys

    reload(sys)
    sys.setdefaultencoding('utf8')
    obj_spider = SpiderMain()
    if len(sys.argv) > 1:
        obj_spider.specified(int(sys.argv[1]))
    else:
        obj_spider.craw()
