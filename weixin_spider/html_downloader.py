# coding:utf8
import urllib2
import oss2
import requests
import config


class HtmlDownloader(object):
    def downloader(self, url):
        if not url: return None
        try:
            response = urllib2.urlopen(url, timeout=3)
        except:
            return None
        if response.code != 200:
            return None
        return response.read()

    def downloader_pic(self, url, file_name):
        #try:
        response = urllib2.urlopen(url, timeout=3)
        with open(file_name, "wb") as f:
            f.write(response.read())
        return file_name
        #except:
        #    return None

    def downloader_pic_uposs(self, url, file_name):
        if url and file_name:
            auth = oss2.Auth(config.ACCESSKEYID, config.ACCESSKEYSECRET)
            bucket = oss2.Bucket(auth, config.ENDPOINT, config.BUCKET)
            input = requests.get(url)
            result = bucket.put_object('images/' + file_name, input)
            return '//static.hstba.com/images/' + file_name if result.status == 200 else ''
