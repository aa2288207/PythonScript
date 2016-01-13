# -*- coding: utf-8

import os
import subprocess

class FileTraversal(object):
    """docstring for FileTraversal"""
    def __init__(self, root_dir, cuckoo_path，commit_type):
        super(FileTraversal, self).__init__()
        self.root_dir = root_dir
        self.cuckoo_path = cuckoo_path
        self.commit_type = commit_type
        
    def file_traversal(self):
        for file in os.listdir(self.root_dir):
            if not os.path.isdir(file):
                cmd = ''
                if self.commit_type == 1:
                    # api提交
                    cmd = 'curl -F file=@%s http://172.16.2.3:8081/tasks/create/intranet_file' % file
                else:
                    # 本地提交
                    cmd = 'python %s/utils/submit.py %s' % (self.cuckoo_path, file)
                print '*'*9
                print cmd
                subprocess.Popen(cmd, shell=True)


def main():
    # 1代表api提交，2代表本地提交
    commit_type = 1
    root_dir = 'D:\works\PyScript'
    cuckoo_path = '/var/VenusAanalysis/cuckoo'
    ft = FileTraversal(root_dir, cuckoo_path, commit_type)
    ft.file_traversal()


if __name__ == '__main__':
    main()