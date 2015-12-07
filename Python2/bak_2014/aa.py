# coding=utf-8
# import re
# str1 = "http://hello.com/a/123/4asd/"
# reg=re.compile(r'http://hello.com(.*)')
# print reg.findall(str1)[0]
import codecs
import pdb


def code_test():
    with codecs.open('./code.conf', 'r') as test:
        context = test.read()
        print context

def code_test2():
    pdb.set_trace()
    print 'xxxx'
    print '---------'
    x = 'xxxp'
    with open('./code.conf', 'wb') as test:
        test.write('[wc]\nfile=中文点.doc\ndesc=测试测试')


import ConfigParser

class Config:
    def __init__(self, cfg):
        """@param cfg: configuration file."""
        config = ConfigParser.ConfigParser(allow_no_value=True)
        config.read(cfg)

        print '--------------'
        for section in config.sections():
            for name, raw_value in config.items(section):
                try:
                    value = config.getboolean(section, name)
                    print value
                except ValueError:
                    try:
                        value = config.getint(section, name)
                    except ValueError:
                        value = config.get(section, name)

                setattr(self, name, value)



def write_file_code():
    with codecs.open('./config.conf', "wb", 'utf-8') as config_file:
        config_file.write('中文')


if __name__ == '__main__':
    # code_test()
    # pdb.run('code_test2()')
    write_file_code()
    # config = Config('analysis.conf')