#!/usr/bin/python3

import abc

def singleton(className):
    from functool import wraps

    instances = {}

    @wraps(className)
    def getinstance(*args, **kwargs):
        if className not in instances:
            instances[className] = className(*args, **kwargs)

        return instances

    return getinstance

class AbstractDB:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def query(self, sql):
        pass

    @abc.abstractmethod
    def execute(self, sql):
        pass

class DBError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class Sqlite(AbstractDB):
    def __init__(self, filename):
        import sqlite3

        self.db = filename

        try:
            self.conn = sqlite3.connect(self.db, check_same_thread=False)
        except:
            raise DBError('failed to connect to sqlite db :{}'.format(self.db))

    def query(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def execute(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()

class DB:

    def __init__(self, dsn):
        self.driver, configString = dsn.split(':', 1)
        
        if self.driver == 'sqlite':
            key, dbfile = configString.split('=', 1)
            if key == 'database':
                self.db = Sqlite(dbfile)
            else:
                raise DBError('unknown dsn key :{}'.format(key))
        else:
            raise DBError('unknown db driver :{}'.format(self.driver))

    def query(self, sql):
        return self.db.query(sql)

    def execute(self, sql):
        self.db.execute(sql)

