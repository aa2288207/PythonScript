# -*- coding:utf-8 -*-


import re


reg = '''<img[^>]+style\\s*=\\s*['\"]([^'\"]+)['\"][^>]*>'''
str_img = '<img style="color: red;" />'

result = re.search(reg, str_img)

print result.groups(0)

