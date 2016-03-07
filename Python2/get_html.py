# -*- coding: utf-8 -*-

import os
import urllib2
import lxml.html as H 

f_error = open('D:\\works\\PycharmProjects\\PythonScript\\Python2\\rsstest\\bb.xml', 'a')

def get_file(url, storage_dir):
    print url
    try:
        response = urllib2.urlopen(url, timeout=10)
        html_str = response.read()
        html = H.document_fromstring(html_str)
        images_src = html.xpath('//img')
        filename = url.split('/')[-1]
        for src in images:
            if src.find('http://static.cnbetacdn.com/article') > -1:
                img_byte = urllib2.urlopen(src, timeout=10)
                img_path = os.path.join(storage_dir, filename)
                if !os.path.exists(img_path)
                    os.makedirs(img_path))
                image_name = src.split('/')[-1]
                with open(os.path.join(img_path, image_name), 'wb') as imgf:
                    imgf.write(img_byte.read())
        
        with open(os.path.join(storage_dir, filename), 'w') as f:
            f.write(html_str)
    except Exception, e:
        f_error.write('%s\t\t\t\t\t\t\terror:\t%s\n' % (url, e))


if __name__ == '__main__':
    url = 'http://rss.cnbeta.com/rss'
    storage_dir = 'D:\\works\\PycharmProjects\\PythonScript\\Python2\\rstest\\'
    get_file(url, storage_dir)