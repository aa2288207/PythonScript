# -*- coding: utf-8 -*-

import feedparser
import get_html


if __name__ == '__main__':
    storage_dir = 'D:\\works\\PycharmProjects\\PythonScript\\Python2\\rsstest\\'
    cnbeta_rss = feedparser.parse('http://rss.cnbeta.com/rss')

    for entrie in cnbeta_rss.entries:
        url = entrie.link
        print url

        get_html.get_file(url, storage_dir)

    get_html.f_error.close()