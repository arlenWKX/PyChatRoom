#--coding:utf-8--
# @Time    : 2020/12/27/027 22:41
# @Author  : panyuangao
# @File    : user_db.py
# @PROJECT : chatRoom
from db import handle_mysql

def checkUser(account):
    sqlite = handle_mysql.SQLite()
    sql_select_account = "SELECT account,password,nickname FROM user WHERE account = '%s'" %account
    userInfo = sqlite.select(sql_select_account)
    sqlite.conn_close()
    return userInfo

def insertUser(account, password, nickname):
    sqlite = handle_mysql.SQLite()
    sql_insert = "INSERT INTO user(account,password,nickname) VALUES('%s','%s','%s')" % (account, password, nickname)
    sqlite.insert(sql_insert)
    sqlite.conn_close()




