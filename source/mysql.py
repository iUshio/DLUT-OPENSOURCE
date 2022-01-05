#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@Author: fionajoyo
@Time: 2022/1/4 
@FileName: mysql.py
"""
from timeit import default_timer

import pymysql

host='116.62.15.29'
port=3306
db='user'
user='user'
password='wsadwsad'

def get_connection():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, password=password)
    return conn

class UsingMysql(object):

    def __init__(self, commit=True, log_time=True, log_label='总用时'):
        self._log_time = log_time
        self._commit = commit
        self._log_label = log_label

    def __enter__(self):

        # 如果需要记录时间
        if self._log_time is True:
            self._start = default_timer()

        # 在进入的时候自动获取连接和cursor
        conn = get_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        conn.autocommit = False

        self._conn = conn
        self._cursor = cursor
        return self

    def __exit__(self, *exc_info):
        # 提交事务
        if self._commit:
            self._conn.commit()
        # 在退出的时候自动关闭连接和cursor
        self._cursor.close()
        self._conn.close()

        if self._log_time is True:
            diff = default_timer() - self._start
            print('-- %s: %.6f 秒' % (self._log_label, diff))

    @property
    def cursor(self):
        return self._cursor



if __name__ == '__main__':
    with UsingMysql(log_time=True) as um:
        um.cursor.execute("select count(id) as total from user")
        data = um.cursor.fetchone()
        print("-- 当前数量: %d " % data['total'])