# -*- coding: utf-8 -*-

import os
import database
import lxml.html as H 

fs = open('F:\\works\\wuyun\\aa.txt', 'w')

sql = 'insert into s_ssvid(number,title,findTime,submitTime,serverity,type,cve_id,cnvd_id,cnnvd_id,author,submitUser,effect) \
       values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'


for parent, dirs, filenames in os.walk('F:\\works\\wuyun\\stest'):
    for filename in filenames:
        with open(os.path.join(parent, filename), 'r') as f:
            html_str = f.read()
            html = H.document_fromstring(html_str)

            number = html.xpath('//dd[@class="text-gray"]//a')[0].text.strip().encode('utf-8')
            title = html.xpath('//h1[1]')[0].text.strip().encode('utf-8')
            findTime = html.xpath('//dd[2]')[0].text.strip().encode('utf-8')
            submitTime = html.xpath('//dd[3]')[0].text.strip().encode('utf-8')
            serverity = ''
            type = html.xpath('//dd[5]/a')[0].text.strip().encode('utf-8')
            cve_id = html.xpath('//dd[6]/a')[0].text.strip().encode('utf-8')
            cnvd_id = html.xpath('//dd[7]/a')[0].text.strip().encode('utf-8')
            cnnvd_id = html.xpath('//dd[8]/a')[0].text.strip().encode('utf-8')
            author = html.xpath('//dd[9]/a')[0].text.strip().encode('utf-8')
            submitUser = html.xpath('//dd[10]/a')[0].text.strip().encode('utf-8')
            effect = html.xpath('//dd[12]')[0].text.strip().encode('utf-8')
            lifeline_list = html.xpath('//ul[@class="list-unstyled"]//*/text()')
            if lifeline_list:
                lifeline = ''.join('%s\n' % ''.join(txt.replace(' ', '').split('\n')).strip() for txt in lifeline_list).strip().encode('utf-8')
            else:
                lifeline = ''

            # values = [number,title,findTime,submitTime,serverity,type,cve_id,cnvd_id,cnnvd_id,author,submitUser,effect]

            print number
            fs.write('%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\neffect:%s\n%s\n' % 
                (number,title,findTime,submitTime,serverity,type,cve_id,cnvd_id,cnnvd_id,author,submitUser,effect,lifeline))

    #         database.cursor.execute(sql, values)
    # database.db.db_commit()
    # database.db.db_close()
 

    
fs.close()

# number
# title
# findTime
# submitTime
# serverity
# type
# cve_id
# cnvd_id
# cnnvd_id
# author
# submitUser
# effect 

# number,title,findTime,submitTime,serverity,type,cve_id,cnvd_id,cnnvd_id,author,submitUser,effect 