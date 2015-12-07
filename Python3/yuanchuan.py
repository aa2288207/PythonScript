import sys
import requests
from bs4 import BeautifulSoup

file = open('yuanchuan.log', 'wb')

index_url = 'http://gepu.kyhs.me/geci/yuanchuan/index.html'
data = requests.get(index_url)
data.encoding = 'gb2312'
soup = BeautifulSoup(data.text, "html.parser")
div = soup.find('div', class_='gepulist')
for link in div.find_all('a'):
    href = link.get('href')
    if not href.find('http://gepu.kyhs.me/geci/yuanchuan/'):
        r = requests.get(href)
        r.encoding = 'gb2312'
        soup2 = BeautifulSoup(r.text, "html.parser")
        div2 = soup2.find('div', class_='gepunr')
        file.write(div2.find('h1').text.encode('utf-8'))
        file.write(div2.text.encode('utf-8'))

file.close()