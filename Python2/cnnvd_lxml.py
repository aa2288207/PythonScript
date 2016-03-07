# -*- coding: utf-8 -*-

from lxml import etree

xmlns = '{http://www.cnnvd.org.cn/vuln/1.0}'

parser = etree.XMLParser(recover=True)
tree = etree.parse('F:\\works\\CNNVD\\xml\\1999_and_before.xml', parser)
root = tree.getroot()
try:
    for elem in root.findall('%sentry' % xmlns):
        vuln_id_node = elem.find('%svuln-id' % xmlns)
        print vuln_id_node.text
except Exception as e:
    print e
finally:
    pass
