# coding:utf8
import re
import urlparse
import uuid

import time
from bs4 import BeautifulSoup

import html_downloader
import html_outputer


class HtmlParser(object):
    def __init__(self):
        self.downloader = html_downloader.HtmlDownloader()
        self.outputer = html_outputer.HtmlOutputer()

    def _get_new_urls(self, soup):
        new_urls = []
        imgBoxs = soup.find_all('div', class_='img-box')
        for ib in imgBoxs:
            link = ib.find('a',
                           href=re.compile(r'http://mp.weixin.qq.com/s\?src=\w+&timestamp=\w+&ver=\w+&signature=\w+'))
            if link:
                img = link.find('img')
                src = img['src'] if img else None
                new_urls.append({'href': link['href'], 'src': src})
        return new_urls

    def _get_new_data(self, html_cont):
        res_data = {}
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        title_node = soup.find('h2', class_='rich_media_title', id="activity-name")
        res_data['title'] = title_node.get_text().strip()
        print res_data['title']
        if self.outputer.is_new_data(res_data['title']):
            return None
        imgs = soup.find('div', class_='rich_media_content', id="js_content").find_all('img')
        for i in imgs:
            file_name = str(uuid.uuid1()) + '.' + i.get('data-type', 'jpg')
            file_oss_url = '//static.hstba.com/images/' + file_name
            self.downloader.downloader_pic_uposs(i['data-src'], file_name)
            i['src'] = file_oss_url
            del i['data-src']
            del i['data-ratio']
            i['width'] = i.get('data-w', '')
            del i['data-w']
            del i['data-type']
        videos = soup.find('div', class_='rich_media_content', id="js_content").find_all('iframe',
                                                                                         class_="video_iframe")
        for v in videos:
            v['src'] = v['data-src']
            del v['data-src']
        res_data['main'] = re.findall(
            r'<div class="rich_media_content " id="js_content">(.+?)</div>(.+?)<script nonce="', str(soup), re.S)[0][
            0].strip()
        return res_data

    def article_parse(self, html_cont):
        if not html_cont: return
        return self._get_new_data(html_cont)

    def url_parse(self, urls_cont):
        if not urls_cont: return
        soup = BeautifulSoup(urls_cont, 'html.parser', from_encoding='utf-8')
        return self._get_new_urls(soup)
