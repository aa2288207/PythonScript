# -*- coding: utf-8 -*-

import os
import MySQLdb

db = MySQLdb.connect("localhost","root","123456","source", 3306, 'utf-8')
cursor = db.cursor()
cursor.execute("SET NAMES utf8");

root_dir = 'F:\\works\\CNNVD\\xml\\'
sql = "insert into s_cnnvd \
(`name`,`cnnvd_id`,`published`,`modified`,`source`, \
`severity`,`cnnvd_type`,`thrtype`,`descript`,`solution`,`cve_id`) \
values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);\n"

for parent, dirs, filenames in os.walk(root_dir):
    for filename in filenames:
        cnnvd_file = open(os.path.join('F:\\works\\CNNVD\\sql', '%s.sql' % filename), 'w')

        with open(os.path.join(parent, filename)) as f:
            content = f.read()
            content_items = content.split('</entry>\n<entry>')
            print len(content_items)
            for item in content_items:
                name_text = item[item.find('<name>')+len('<name>'):item.find('</name>')]
                cnnvd_id_text = item[item.find('<vuln-id>')+len('<vuln-id>'):item.find('</vuln-id>')]
                published_text = item[item.find('<published>')+len('<published>'):item.find('</published>')]
                modified_text = item[item.find('<modified>')+len('<modified>'):item.find('</modified>')]
                source_text = item[item.find('<source>')+len('<source>'):item.find('</source>')]
                severity_text = item[item.find('<severity>')+len('<severity>'):item.find('</severity>')]
                vuln_type_text = item[item.find('<vuln-type>')+len('<vuln-type>'):item.find('</vuln-type>')]
                thrtype_text = item[item.find('<thrtype>')+len('<thrtype>'):item.find('</thrtype>')]
                vuln_descript_text = item[item.find('<vuln-descript>')+len('<vuln-descript>'):item.find('</vuln-descript>')]
                cve_id_text = item[item.find('<cve-id>')+len('<cve-id>'):item.find('</cve-id>')]
                vuln_solution_text = item[item.find('<vuln-solution>')+len('<vuln-solution>'):item.find('</vuln-solution>')]

                # cncpe 处理
                cncpe_text = item[item.find('<cncpe ')+len('<cncpe '):item.find('</cncpe>')]
                cncpe_items = cncpe_text.split('<cncpe-lang ')
                for c_item in cncpe_items:
                    if c_item.find('name="') != -1:
                        c_text = c_item[c_item.find('name="')+len('name="'):c_item.find('"/>')]
                        if c_text != '':
                            cursor.execute('insert into s_cnnvd_cncpe(cnnvd_id, cncpe_name) values(%s, %s)',
                                [cnnvd_id_text, c_text])

                product_text = item[item.find('<vuln-software-list>')+len('<vuln-software-list>'):item.find('</vuln-software-list>')]
                product_items = product_text.split('<product>')
                for p_item in product_items:
                    p_text = p_item[:p_item.find('</product>')]
                    if p_text != '':
                        cursor.execute('insert into s_cnnvd_software(cnnvd_id, product) values(%s, %s)',
                            [cnnvd_id_text, p_text])

                refs_text = item[item.find('<refs>')+len('<refs>'):item.find('</refs>')]
                refs_items = refs_text.split('</ref>\n<ref>')
                for r_item in refs_items:
                    ref_source = r_item[r_item.find('<ref-source>')+len('<ref-source>'):r_item.find('</ref-source>')]
                    ref_name = r_item[r_item.find('<ref-name>')+len('<ref-name>'):r_item.find('</ref-name>')]
                    ref_url = r_item[r_item.find('<ref-url>')+len('<ref-url>'):r_item.find('</ref-url>')]
                    cursor.execute('insert into s_cnnvd_refs(cnnvd_id, ref_source, ref_name, ref_url) values(%s, %s, %s, %s)',
                        [cnnvd_id_text, ref_source, ref_name, ref_url])

                values = [name_text,
                    cnnvd_id_text,
                    published_text,
                    modified_text,
                    source_text,
                    severity_text,
                    vuln_type_text,
                    thrtype_text,
                    vuln_descript_text,
                    vuln_solution_text,
                    cve_id_text]
                
                cursor.execute(sql, values)
                # cnnvd_file.write(result)
            db.commit()

        cnnvd_file.close()
db.close()