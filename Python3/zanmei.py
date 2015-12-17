import sys
import requests
from bs4 import BeautifulSoup


file = open('context1.log', 'ab')
try:
    for x in range(1, 401):
        if x < 10:
            xx = '00%d' % x
        elif 10 <= x < 100:
            xx = '0%d' % x
        else:
            xx = x
        url = 'http://www.jonahome.net/files/zmsg/zmsgc/zhanmeishi/Hymn%s.htm' % xx
        r = requests.get(url)
        r.encoding = 'gb2312'
        soup = BeautifulSoup(r.text, "html.parser")

        txt = soup.find('div', class_='TitleLinks').text
        title = txt[txt.find("《"): txt.find("》")+1]
        content = txt[txt.find("》")+1:].replace('\r\n', '<br>')
        sql = "insert into hymn(hid, title,content) values('%s', %s','%s');\r\n" % (xx, title, content)
        file.write(sql.encode('utf-8'))
        print(x)
        print(url)
finally:
    file.close()
