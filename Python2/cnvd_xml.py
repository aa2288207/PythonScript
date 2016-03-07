# -*- coding: utf-8 -*-

import MySQLdb
import traceback
from lxml import etree


db = MySQLdb.connect("localhost","root","123456","source", 3306, charset='utf8')
cursor = db.cursor()


sql = "insert into s_cnvd(number,title,description,formalWay,tempWay,isFirst,referenceLink,isZero,manufacturer,dateCreated,submitTime,storageTime,openTime,foundTime,cveStr,bidStr,cause,thread,serverity,position,softStyle,reporter,isHot,isOriginal,discovererName,isv,exploitName,exploitTuser,exploitConcept,poc,exploitSuggestion,exploitTime,exploitRefer,ivp,patchId,patchName,patchInfoTuser,patchDescription,function,patchUrl,score,baseMetric,reflectProduct) \
       values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

tree = etree.parse('F:\\works\\CNVD\\xml\\2016.xml')
root = tree.getroot()

try:
    for elem in root.findall('flawInfo'):
        values = [
                elem.find('number').text,
                elem.find('title').text,
                elem.find('description').text,
                elem.find('formalWay').text,
                elem.find('tempWay').text,
                elem.find('isFirst').text,
                elem.find('referenceLink').text,
                elem.find('isZero').text,
                elem.find('manufacturer').text,
                elem.find('dateCreated').text,
                elem.find('submitTime').text,
                elem.find('storageTime').text,
                elem.find('openTime').text,
                elem.find('foundTime').text,
                elem.find('cveStr').text,
                elem.find('bidStr').text,
                elem.find('cause').text,
                elem.find('thread').text,
                elem.find('serverity').text,
                elem.find('position').text,
                elem.find('softStyle').text,
                elem.find('reporter').text,
                elem.find('isHot').text,
                elem.find('isOriginal').text,
                elem.find('discovererName').text,
                elem.find('isv').text,
                elem.find('exploitName').text,
                elem.find('exploitTuser').text,
                elem.find('exploitConcept').text,
                elem.find('poc').text,
                elem.find('exploitSuggestion').text,
                elem.find('exploitTime').text,
                elem.find('exploitRefer').text,
                elem.find('ivp').text,
                elem.find('patchId').text,
                elem.find('patchName').text,
                elem.find('patchInfoTuser').text,
                elem.find('patchDescription').text,
                elem.find('function').text,
                elem.find('patchUrl').text,
                elem.find('score').text,
                elem.find('baseMetric').text,
                elem.find('reflectProduct').text
        ]
        # print elem.find('number').text
        cursor.execute("SET NAMES utf8");
        cursor.execute(sql, values)
    db.commit()
except Exception as e:
    print e
    print traceback.format_exc()
finally:
    cursor.close()
    db.close()



# number,title,description,formalWay,tempWay,isFirst,referenceLink,isZero,manufacturer,dateCreated,submitTime,storageTime,openTime,foundTime,cveStr,bidStr,cause,thread,serverity,position,softStyle,reporter,isHot,isOriginal,discovererName,isv,exploitName,exploitTuser,exploitConcept,poc,exploitSuggestion,exploitTime,exploitRefer,ivp,patchId,patchName,patchInfoTuser,patchDescription,function,patchUrl,score,baseMetric,reflectProduct


# number,
# title,
# description,
# formalWay,
# tempWay,
# isFirst,
# referenceLink,
# isZero,
# manufacturer,
# dateCreated,
# submitTime,
# storageTime,
# openTime,
# foundTime,
# cveStr,
# bidStr,
# cause,
# thread,
# serverity,
# position,
# softStyle,
# reporter,
# isHot,
# isOriginal,
# discovererName,
# isv,
# exploitName,
# exploitTuser,
# exploitConcept,
# poc,
# exploitSuggestion,
# exploitTime,
# exploitRefer,
# ivp,
# patchId,
# patchName,
# patchInfoTuser,
# patchDescription,
# function,
# patchUrl,
# score,
# baseMetric,
# reflectProduct