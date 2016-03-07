# -*- coding: utf-8 -*-

import os
import database
import lxml.html as H 

# fs = open('F:\\works\\wuyun\\test\\aa.txt', 'w')

sql = 'insert into s_wooyun(number,title,firm,author,submitTime,openTime,type,serverity,rank,status,source,tags) \
       values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'


for parent, dirs, filenames in os.walk('F:\\works\\wuyun\\wooyun\\achieve'):
    for filename in filenames:
        with open(os.path.join(parent, filename), 'r') as f:
            html_str = f.read()
            html = H.document_fromstring(html_str)

            number = html.xpath('//div[@class="content"]//h3[1]//a')[0].text.strip().encode('utf-8')
            title = html.xpath('//div[@class="content"]//h3[@class="wybug_title"]')[0].text.replace(u'漏洞标题：', '').strip().encode('utf-8')
            firm = html.xpath('//div[@class="content"]//h3[@class="wybug_corp"]//a')[0].text.strip().encode('utf-8')
            author = html.xpath('//div[@class="content"]//h3[@class="wybug_author"]//a')[0].text.strip().encode('utf-8')
            submitTime = html.xpath('//div[@class="content"]//h3[@class="wybug_date"]')[0].text.replace(u'提交时间：', '').strip().encode('utf-8')
            openTime = html.xpath('//div[@class="content"]//h3[@class="wybug_open_date"]')[0].text.replace(u'公开时间：', '').strip().encode('utf-8')
            type = html.xpath('//div[@class="content"]//h3[@class="wybug_type"]')[0].text.replace(u'漏洞类型：', '').strip().encode('utf-8')
            serverity = html.xpath('//div[@class="content"]//h3[@class="wybug_level"]')[0].text.replace(u'危害等级：', '').strip().encode('utf-8')
            rank = html.xpath('//div[@class="content"]//h3[9]')[0].text.replace(u'自评Rank：', '').strip().encode('utf-8')
            status = html.xpath('//div[@class="content"]//h3[@class="wybug_status"]')[0].text.replace(u'漏洞状态：', '').strip().encode('utf-8')
            source = html.xpath('//div[@class="content"]//h3[11]//a/@href')[0].strip().encode('utf-8')
            tags_list = html.xpath('//div[@class="content"]//h3[12]//span//a/text()')
            tags = '\n'.join(txt for txt in tags_list).strip().encode('utf-8')

            values = [number,title,firm,author,submitTime,openTime,type,serverity,rank,status,source,tags]

            print number
            database.cursor.execute(sql, values)
    database.db.db_commit()
    database.db.db_close()
    # disclosure_list = html.xpath('//div[@class="content"]//p[@class="detail wybug_open_status"]/text()')
    # disclosure = '\n'.join(txt.strip() for txt in disclosure_list).strip().encode('utf-8')

    # description_list = html.xpath('//div[@class="content"]//p[@class="detail wybug_description"]/text()')
    # description = '\n'.join(txt.strip() for txt in description_list).strip().encode('utf-8')

    # detailed_list = html.xpath('//div[@class="content"]//div[@class="wybug_detail"]//p[@class="detail"]/text()')
    # detailed = '\n'.join(txt.strip() for txt in detailed_list).strip().encode('utf-8')

    # prove_list = html.xpath('//div[@class="content"]//div[@class="wybug_poc"]/*/text()')
    # prove = '\n'.join(txt.strip() for txt in prove_list).strip().encode('utf-8')

    # repair_list = html.xpath('//div[@class="content"]//div[@class="wybug_patch"]//p[@class="detail"]/text()')
    # repair = '\n'.join(txt.strip() for txt in repair_list).strip().encode('utf-8')

    # copyright_list = html.xpath('//div[@class="content"]//h3[19]//text()')
    # copyright = ''.join(txt for txt in copyright_list).strip().encode('utf-8')

    # vendorsRespond_list = html.xpath('//div[@class="content"]//div[@class="bug_result"]/*/text()')
    # vendorsRespond = '\n'.join(txt.strip() for txt in vendorsRespond_list).strip().encode('utf-8')
    # vendorReply,
    # latestState,

    # fs.write('%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s' % 
    #         (number,title,firm,author,submitTime,openTime,type,serverity,rank,status,source,tags,
    #             disclosure,description,detailed,prove,repair,copyright,vendorsRespond))

# fs.close()

# number,
# title,
# firm,
# author,
# submitTime,
# openTime,
# type,
# serverity,
# rank,
# status,
# source,
# tags,
# disclosure,
# description,
# detailed,
# prove,
# repair,
# copyright,
# vendorsRespond,
# vendorReply,
# latestState,


# number,title,firm,author,submitTime,openTime,type,serverity,rank,status,source,tags,disclosure,description,detailed,prove,repair,copyright,vendorsRespond,vendorReply,latestState,