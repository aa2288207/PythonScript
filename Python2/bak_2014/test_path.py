# -*- coding: utf-8 -*-

import sys
print sys.path[0]


import test_class



class WangChuang(object):
    """docstring for WangChuang"""

    def get(self):
        test_class.aa()


if __name__ == '__main__':
    wc = WangChuang()
    wc.get()