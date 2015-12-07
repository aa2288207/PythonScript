import sys
import io
import pymysql
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stdin = io.TextIOWrapper(sys.stdin.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', db='tyhp', charset='utf8')

try:
    cur = connection.cursor()
    context = open('../static/t_cnnvd_part_2.sql', encoding='utf-8').read()
    c_list = context.split('INSERT INTO t_cnnvd (cnnvdid, vulnname, published, modified, severity,vulnsoft, cveid, referenceurl, reporter, patch, resolution, description) VALUES(\'')
    for c in c_list:
        c = c.replace('\');', '')
        tmp = c.split('\', \'')
        print(len(tmp))
        if len(c) > 1:
            sql = "INSERT INTO t_bug (cnnvdNo, name, capTime, bugLeave, entity, cveNo, about) " \
                  "VALUES('%s','%s','%s','%s','%s','%s','%s')" % (tmp[0].replace('-CNNVD-', '-'),tmp[1].replace('\'', '-1~1-'),tmp[2],tmp[4],tmp[5],tmp[6],tmp[11].replace('\'', '-1~1-'))
            cur.execute(sql)

    connection.commit()
finally:
    connection.close()
