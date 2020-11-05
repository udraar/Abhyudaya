import warnings
import pymysql

class Database(object):
    DB_Host = 'localhost'
    DB_User = 'abhyudaya'
    Pswd = 'abhyudaya123'
    DB_Name = 'abhyudaya'
    DB_Client = None

    @staticmethod
    def initialize():
        Database.DB_Client = pymysql.connect(host=Database.DB_Host, user=Database.DB_User, pasword=Database.Pswd, db=Database.DB_Name)


    @staticmethod
    def insert(table, **data):
        cols = "`,`".join([str(i) for i in data.columns.tolist()])
        sql = f"INSERT INTO {table}"

