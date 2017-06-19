# -*- coding: utf-8 -*-
import MySQLdb as mysql

try:
    conn = MySQLdb.connect(host='localhost', user='root',
                           passwd='', db='llbuaa', port=3306)
    cur = conn.cursor()
    # sheet
    cur.execute('select * from morning_balance_sheet')
    # get one line
    one = cur.fetchone()

    # unit
    cur.execute('select * from morning_unit')
    cur.close()
    conn.close()
except MySQLdb.Error, e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])


# for labeling one company
def label_one_company(company_id):
    return lable


def label_all_company():
    return
