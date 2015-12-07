# -*- coding: utf-8

import os
import urllib2

try:
    from poster.encode import multipart_encode
    from poster.streaminghttp import register_openers
except Exception, e:
    print 'Please execute pip install poster'


class FileTraversal(object):
    """docstring for FileTraversal"""

    def file_traversal(self, root_dir=''):
        for file in os.listdir(root_dir):
            path = os.path.join(root_dir, file)
            print path
            if os.path.isdir(path):
                self.file_traversal(path)
            else:
                register_openers()
                datagen, headers = multipart_encode({'file': open(path, 'rb')})
                request = urllib2.Request('http://172.16.2.4:8081/tasks/create/intranet_file', datagen, headers)
                print '*'*9
                print urllib2.urlopen(request).read()

def main():
    root_dir = 'D:\\works\\PyScript\\aa'
    ft = FileTraversal()
    ft.file_traversal(root_dir)


if __name__ == '__main__':
    main()