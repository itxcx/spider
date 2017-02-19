# coding:utf8
import re
import urlparse
import uuid

import time
from bs4 import BeautifulSoup

import html_downloader
import html_outputer


class HtmlParser(object):
    def __init__(self,database_connect):
        self.downloader = html_downloader.HtmlDownloader()
        self.outputer = html_outputer.HtmlOutputer(database_connect)

    def _get_new_urls(self, soup):
        new_urls = set()
        links = soup.find_all('a', href=re.compile(
            r'http://mp.weixin.qq.com/s\?src=\w+&timestamp=\w+&ver=\w+&signature=\w+'))
        for link in links:
            new_url = link['href']
            new_urls.add(new_url)
        return new_urls

    def _get_new_data(self, html_cont):
        res_data = {}
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        title_node = soup.find('h2', class_='rich_media_title', id="activity-name")
        res_data['title'] = title_node.get_text().strip()
        if self.outputer.is_new_data(res_data['title']):
            return None
        imgs = soup.find('div', class_='rich_media_content', id="js_content").find_all('img')
        for i in imgs:
            file_name = ('wp-content/uploads/%s/%s/' % (
                time.strftime('%Y', time.localtime(time.time())),
                time.strftime('%m', time.localtime(time.time())),)) + str(
                uuid.uuid1()) + '.' + i.get('data-type', 'jpg')
            self.downloader.downloader_pic(i['data-src'], file_name)
            i['src'] = '/' + file_name
            del i['data-src']
            del i['data-ratio']
            i['width'] = i.get('data-w', '')
            del i['data-w']
            del i['data-type']
        res_data['main'] = re.findall(
            r'<div class="rich_media_content " id="js_content">(.+?)</div>(.+?)<script nonce="', str(soup), re.S)[0][0].strip()
        return res_data

    def article_parse(self, html_cont):
        if not html_cont: return
        return self._get_new_data(html_cont)

    def url_parse(self, urls_cont):
        if not urls_cont: return
        soup = BeautifulSoup(urls_cont, 'html.parser', from_encoding='utf-8')
        return self._get_new_urls(soup)
