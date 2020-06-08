# -*- coding: UTF-8 -*-
"""
1、执行带参数的ＳＱＬ时，请先用sql语句指定需要输入的条件列表，然后再用tuple/list进行条件批配
２、在格式ＳＱＬ中不需要使用引号指定数据类型，系统会根据输入参数自动识别
３、在输入的值中不需要使用转意函数，系统会自动处理
"""

import pymysql
from DBUtils.PooledDB import PooledDB
from pymysql.cursors import DictCursor

from config.iniutils import GetIni

"""
Config是一些数据库的配置文件
"""


class Mysql(object):
    """
    MYSQL数据库对象，负责产生数据库连接 , 此类中的连接采用连接池实现获取连接对象：conn = Mysql.getConn()
            释放连接对象;conn.close()或del conn
    """
    # 连接池对象
    pool = None

    def __init__(self, sec):
        ini = GetIni('config.ini', r'C:\workspaces\python\pyprojects\python-practices')
        kvs = ini.get_kvs(sec)
        # 数据库构造函数，从连接池中取出连接，并生成操作游标
        if self.pool is None:
            self.pool = PooledDB(creator=pymysql, mincached=1, maxcached=int(kvs['maxconnect']),
                              host=kvs['dbhost'], port=int(kvs['dbport']), user=kvs['dbuser'], passwd=kvs['dbpwd'],
                              db=kvs['dbname'], use_unicode=True, charset=kvs['dbchar'],
                                 cursorclass=DictCursor)

    def get_conn(self):
        return self.pool.connection()

    def getAll(self, sql, param=None):
        conn = self.pool.connection()
        cursor = conn.cursor()
        if param is None:
            count = cursor.execute(sql)
        else:
            count = cursor.execute(sql, param)
        if count > 0:
            result = cursor.fetchall()
        else:
            result = None
        cursor.close()
        conn.close()
        return result

    def getOne(self, sql, param=None):
        conn = self.pool.connection()
        cursor = conn.cursor()
        if param is None:
            count = cursor.execute(sql)
        else:
            count = cursor.execute(sql, param)
        if count > 0:
            result = cursor.fetchone()
        else:
            result = None
        cursor.close()
        conn.close()
        return result

    def update_one(self, sql, param=None):
        conn = self.pool.connection()
        cursor = conn.cursor()
        try:
            if param is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, param)
            conn.commit()
        except Exception as err:
            print(err)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def getMany(self, sql, num, param=None):
        conn = self.pool.connection()
        cursor = conn.cursor()
        if param is None:
            count = cursor.execute(sql)
        else:
            count = cursor.execute(sql, param)
        if count > 0:
            result = cursor.fetchmany(num)
        else:
            result = None
        cursor.close()
        conn.close()
        return result

    def createTable(self, sql):
        conn = self.pool.connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            conn.commit()
        except Exception as err:
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    # 直接提交的插入
    def insertOne(self, sql, value):
        conn = self.pool.connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, value)
            conn.commit()
        except Exception as err:
            print(err)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
        return self.__getInsertId()

    def insertMany(self, sql, values):
        count = None
        conn = self.pool.connection()
        cursor = conn.cursor()
        try:
            count = cursor.executemany(sql, values)
            conn.commit()
        except Exception as err:
            print(err)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
        return count

    def __getInsertId(self):
        conn = self.pool.connection()
        cursor = conn.cursor()
        cursor.execute("SELECT @@IDENTITY AS id")
        result = cursor.fetchall()
        return result[0]['id']

