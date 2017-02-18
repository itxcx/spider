# coding:utf8
import os

import time


class HtmlOutputer(object):
    def __init__(self):
        self.datas = []
    
    def collect_data(self, data):
        if data:
            self.datas.append(data)

    def output_html(self):
        fileName = "output-%s.html" % str(int(time.time()))
        if os.path.exists(fileName):
            os.remove(fileName)
        fout = open(fileName,'w')
        fout.write('<html>')

        fout.write('<body>')

        fout.write('<table>')
        for data in self.datas:
            fout.write('<tr>')
            fout.write('<td>%s</td>' % data['url'].encode('utf-8'))
            fout.write('<td>%s</td>' % data['title'].encode('utf-8'))
            fout.write('<td>%s</td>' % data['summary'].encode('utf-8'))
            fout.write('</tr>')

        fout.write('</table>')

        fout.write('</body>')

        fout.write('</html>')