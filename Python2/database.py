# -*- coding: utf-8 -*-

import MySQLdb

db = MySQLdb.connect("localhost","root","123456","source", 3306, charset='utf8')
cursor = db.cursor()


def db_commit():
    db.commit()

def db_close():
    cursor.close()
    db.close()

