# coding:utf8

class UrlManager(object):
    def __init__(self):
        self.new_urls = []

    def url_collector(self, index):
        self.new_urls = []
        index = str(index)
        return (
            'http://weixin.sogou.com/pcindex/pc/pc_' + index + '/pc_' + index + '.html',
            #'http://weixin.sogou.com/pcindex/pc/pc_' + index + '/1.html',
            #'http://weixin.sogou.com/pcindex/pc/pc_' + index + '/2.html',
            #'http://weixin.sogou.com/pcindex/pc/pc_' + index + '/3.html',
            #'http://weixin.sogou.com/pcindex/pc/pc_' + index + '/4.html',
        )

    def add_new_url(self, url):
        if url and url not in self.new_urls:
            self.new_urls.append(url)

    def add_new_urls(self, new_urls):
        if new_urls:
            for url in new_urls:
                self.add_new_url(url)

    def has_new_url(self):
        return len(self.new_urls) != 0

    def get_new_url(self):
        new_url = self.new_urls.pop()
        return new_url

