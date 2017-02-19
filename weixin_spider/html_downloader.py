# coding:utf8
import urllib2


class HtmlDownloader(object):
    def downloader(self, url):
        if not url: return
        response = urllib2.urlopen(url, timeout=1)
        if response.code != 200:
            return None
        return response.read()

    def downloader_pic(self, url, file_name):
        try:
            response = urllib2.urlopen(url)
            with open(file_name, "wb") as f:
                f.write(response.read())
            return file_name
        except:
            return None
