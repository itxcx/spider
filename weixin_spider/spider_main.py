# coding:utf8
import random
import time

import MySQLdb

import url_manager, html_downloader, html_parser, html_outputer


class SpiderMain(object):
    def __init__(self):
        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="hstba", charset="utf8")
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parse = html_parser.HtmlParser(db)
        self.outputer = html_outputer.HtmlOutputer(db)


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
                    print 'craw %d : %s' % (count, new_url,)
                    html_cont = self.downloader.downloader(new_url)
                    new_data = self.parse.article_parse(html_cont)
                    if new_data is None: continue
                    self.outputer.collect_data(new_data, index + 1)
                    count = count + 1
                    sleep = int(random.random() * 8)
                    print 'sleep in %s' % sleep
                    time.sleep(sleep)
                except Exception, e:
                    print Exception, ":", e
                    print 'craw failed'
            print 'category ' + str(index) + ' finish'
            self.outputer.close_db()


if __name__ == "__main__":
    import sys

    reload(sys)
    sys.setdefaultencoding('utf8')
    obj_spider = SpiderMain()

    obj_spider.craw()
