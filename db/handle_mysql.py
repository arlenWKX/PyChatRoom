#--coding:utf-8--
# @Time    : 2020/12/27/027 22:25
# @Author  : panyuangao
# @File    : handle_mysql.py
# @PROJECT : chatRoom

import sqlite3
from os.path import exists
class SQLite():
    def __init__(self):
        if not exists('chat.db'):
            self.conn = sqlite3.connect('chat.db')
            self.conn.execute('CREATE TABLE user(account TEXT NOT NULL,password TEXT NOT NULL,nickname TEXT NOT NULL);')
            self.conn.commit()
        else:
            self.conn = sqlite3.connect('chat.db')
        self.conn = sqlite3.connect('chat.db')

    def insert(self,SQL):
        cursor = self.conn.cursor()
        cursor.execute(SQL)
        cursor.close()
        self.conn.commit()

    def select(self,SQL):
        cursor = self.conn.cursor()
        cursor.execute(SQL)
        resSet = cursor.fetchall()
        cursor.close()
        self.conn.commit()
        return resSet
    def conn_close(self):
        self.conn.close()  # 第六步：关闭连接


if __name__ == '__main__':
    sqlite = SQLite()
    sql = "SELECT nickname FROM user "
    resSet = sqlite.select(sql)
    print(resSet[0][0])
