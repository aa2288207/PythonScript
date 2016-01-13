# -*- coding:utf-8



import os


def ishan(text):
    # for python 2.x, 3.3+
    # sample: ishan(u'一') == True, ishan(u'我&&你') == False
    return all(u'\u4e00' <= char <= u'\u9fff' for char in text)
    # return all(u'\uFE30' <= char <= u'\uFFA0' for char in text)
    # return all(u'\uFE30' <= char <= u'\uFFA0' for char in text)

def isfuhao(text):
    # 标点符号
    return all(u'\uFF00' <= char <= u'\uFFEF' for char in text)
            

def guhao(text):
    # 句号
    return all(u'\u2E80' <= char <= u'\uFE4F' for char in text)

rootdir = 'E:\\zxl\\22'
outdir = 'E:\\zxl\\pdf'

for parent, dirs, filenames in os.walk(rootdir):
    for filename in filenames:
        rootfile = os.path.join(parent,filename)

        f2 = open('E:\\zxl\\pdf\\%s' % filename, 'w')


        with open(rootfile, 'r') as f:
            context = f.read()
            i = 0
            for char in context:
                i = i + 1
                if ishan(char):
                    f2.write(char.encode('utf-8'))
                elif isfuhao(char):
                    f2.write(char.encode('utf-8'))
                elif guhao(char):
                    f2.write(char.encode('utf-8'))
                if i == 100:
                    f2.write('--utf--')



        f2.close()