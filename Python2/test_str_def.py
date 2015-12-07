# -*- coding: utf-8 


def ab(arg1,arg2):
    print arg2,arg1
    return arg1

def abc(arg1,arg2):
    print arg2+arg1
    return arg1+arg2

if __name__ == '__main__':
    # d = abc
    # l = [d, abc]
    # print type(l[0])
    # l[0](3,88)
    # l = ['ab', 'abc']
    # print type(l[0])
    # eval(l[0])(3,88)
    # # print 'xxxxxx'
    # # eval(l[1])(113,188)

    aa = '\xef\xbf\x84\xef\xbf\xa3\xef\xbf\x8a\xef\xbf\x87'
    print aa.decode('utf-8', 'ignore')