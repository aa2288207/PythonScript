# -*- coding: utf-8 -*-

import os

root_dir = os.path.join(os.getcwd())

def main(root_dir):
    """ 遍历目录文件 

        Args:
            root_dir: 查找的根目录

        Return:
            root: 目录的绝对路径
            dirs: 目录名的集合
            files: 文件名的集合
    """
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            print os.path.join(root, file)


if __name__ == '__main__':
    root_dir = 'D:\works\PyScript'
    main(root_dir)