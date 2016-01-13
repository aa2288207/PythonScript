# -*- coding:utf-8 -*-


x = 0
hid = ''
title = ''
txt = []
sql = "insert into hymn(hid, title, content, pid) values('%s', '%s', '%s', 2);\n"

f2 = open('E:\\zxl\\2.md.sql', 'w')

with open('E:\\zxl\\2.md.txt', 'r') as f:
    for content in f.readlines():
        if content.find('##') != -1:
            txt.append(content.replace('##副歌', '(副歌)'))
        elif content.find('#') != -1:
            f2.write(sql % (hid, title, '\n'.join(txt)))
            x = x + 1
            if x < 10:
                xx = '00%d' % x
            elif 10 <= x < 100:
                xx = '0%d' % x
            else:
                xx = x

            hid = xx
            txt = []
            title = content.split(' ')[1]
        else:
            content = content.replace('\n', '')
            if content != '':
                txt.append(content)
            txt.append('<br>')


f2.close()
