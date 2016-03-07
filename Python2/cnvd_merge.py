# -*- coding: utf-8 -*-

import MySQLdb

db = MySQLdb.connect("localhost","root","123456","source", 3306, charset='utf8')
cursor = db.cursor()

cursor.execute('select cnvdid from t_cnvd')

for row in cursor.fetchall():
    r = cursor.execute('select number from s_cnvd where number=%s', row[0])
    if r >= 1:
        print row[0]
        cursor.execute('delete from t_cnvd where cnvdid=%s', row[0])
    else:
        print r

db.commit()
cursor.close()
db.close()