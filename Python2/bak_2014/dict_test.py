# -*- coding: utf-8 -*-

dict = {"a" : "apple", "b" : "grape", "c" : "orange", "d" : "banana"}

print dict


ls = [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]  

print ls
ls.sort(key=lambda key:key[1])
print ls