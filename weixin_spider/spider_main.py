# coding:utf8
import random
import time
import uuid

import url_manager, html_downloader, html_parser, html_outputer


class SpiderMain(object):
    def __init__(self):
        self.db = None
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parse = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self):
        count = 1
        category_total = 20
        for index in range(category_total):
            # 收集本栏目的全部url
            collectors = self.urls.url_collector(index)
            for collector in collectors:
                urls_cont = self.downloader.downloader(collector)
                urls = self.parse.url_parse(urls_cont)
                self.urls.add_new_urls(urls)
            while self.urls.has_new_url():
                try:
                    new_url = self.urls.get_new_url()
                    print 'craw %d : %s' % (count, new_url['href'],)
                    html_cont = self.downloader.downloader(new_url['href'])
                    new_data = self.parse.article_parse(html_cont)
                    if new_data is None: continue
                    thumbnail_uuid = str(
                        uuid.uuid1())
                    file_name_base = ('wp-content/uploads/%s/%s/' % (
                        time.strftime('%Y', time.localtime(time.time())),
                        time.strftime('%m', time.localtime(time.time())),)) + thumbnail_uuid;
                    file_name = file_name_base + '.jpeg'
                    file_name_150 = file_name_base + '-150x150.jpeg'
                    file_name_300 = file_name_base + '-300x169.jpeg'
                    if new_url['src']:
                        src = new_url['src']
                        thumbnail = self.downloader.downloader_pic(src, file_name)
                        if not thumbnail:
                            thumbnail_uuid = None
                    else:
                        thumbnail_uuid = None
                    self.outputer.collect_data(new_data, thumbnail_uuid, index + 1)
                    count = count + 1
                    sleep = int(random.random() * 8)
                    print 'sleep in %s' % sleep
                    time.sleep(sleep)
                except Exception, e:
                    print Exception, ":", e
                    print 'craw failed'
            print 'category ' + str(index) + ' finish'


if __name__ == "__main__":
    import sys

    reload(sys)
    sys.setdefaultencoding('utf8')
    obj_spider = SpiderMain()

    obj_spider.craw()
