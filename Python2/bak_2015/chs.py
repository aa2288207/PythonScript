# -*- coding:utf-8

def is_cn_char(i): 
    return 0x4e00<=ord(i)<0x9fa6 


def ishan(text):
    # for python 2.x, 3.3+
    # sample: ishan(u'一') == True, ishan(u'我&&你') == False
    return all(u'\u4e00' <= char <= u'\u9fff' for char in text)


def isfuhao(text):
    for char in text:
        if char == '\u3002':
            return True
        elif char == '\uFF1F':
            return True
        elif char == '\uFF01':
            return True
        elif char == '\uFF0C':
            return True
        elif char == '\u3001':
            return True
        elif char == '\uFF1B':
            return True
        elif char == '\uFF1A':
            return True
        elif char == '\u300C':
            return True
        elif char == '\u300D':
            return True
        elif char == '\u300E':
            return True
        elif char == '\u300F':
            return True
        elif char == '\u2018':
            return True
        elif char == '\u2019':
            return True
        elif char == '\u201C':
            return True
        elif char == '\u201D':
            return True
        elif char == '\uFF08':
            return True
        elif char == '\uFF09':
            return True
        elif char == '\u3014':
            return True
        elif char == '\u3015':
            return True
        elif char == '\u3010':
            return True
        elif char == '\u3011':
            return True
        elif char == '\u2014':
            return True
        elif char == '\u2026':
            return True
        elif char == '\u2013':
            return True
        elif char == '\uFF0E':
            return True
        elif char == '\u300A':
            return True
        elif char == '\u300B':
            return True
        elif char == '\u3008':
            return True
        elif char == '\u3009':
            return True
        else:
            return all(u'\uFE30' <= char <= u'\uFFA0' for char in text)

if __name__ == '__main__':
    s = '忘啊孙大发大水法大水法'
    s = s.decode("utf-8")
    # for char in s:
    #     print type(char)
    #     print ishan(char)

    b = '，。：；“”'
    b = b.decode("utf-8")
    for char in b:
        print isfuhao(char)

