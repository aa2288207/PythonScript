# -*- coding:utf-8

import os

outfile = 'E:\\zxl\\22tt\\aa.txt'
rootdir = 'E:\\zxl\\pdf'
sql = 'insert into hymn(title, content, pid) value("%s", "%s", 2);\n'

f2 = open(outfile, 'w')

for parent, dirs, filenames in os.walk(rootdir):
    for filename in filenames:
        rootfile = os.path.join(parent,filename)

        with open(rootfile, 'r') as f:
            context = f.read()
            text = context.split('--utf--');
            if text:
                f2.write(sql % (text[0], text[1]))
            else:
                print '--------%s' % context


f2.close()