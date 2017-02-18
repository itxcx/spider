# coding:utf8
import urllib2


class HtmlDownloader(object):
    def downloader(self, url):
        if not url: return
        my_headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Host": "baike.baidu.com",
            'Referer': 'https://www.baidu.com/link?url=NetgrT-_ghcfSSmozgeH4UKok6FBqc1Cibdt6z17HxA3XkPPhyu2Dn0tDByqSJnvq1DEv5rq1BfVWl6GucBqAK&wd=&eqid=eefdb9b5001c5b140000000258a83e40',
            "GET": url
        }
        req = urllib2.Request(url, headers=my_headers)

        response = urllib2.urlopen(req, timeout=1)
        if response.code != 200:
            return None
        return response.read()
