# -*- coding:utf-8 -*-


def deco(func):
    def _deco():
        print 'before'
        func()
        print 'after'
    return _deco


@deco
def myfunc():
    print 'myfunc() called'


def deco2(func):
    print 'before'
    func()
    print 'after'
    return func



def myfunc2():
    print 'myfunc2() called'


if __name__ == '__main__':
    myfunc2()
    cc = deco2(myfunc2)
    cc()
    myfunc2()