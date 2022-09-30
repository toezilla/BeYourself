import os
import pymysql
from dotenv import load_dotenv

class GetDB:
    def __init__(self):
        self.conn = pymysql.connect(
            host=DBInfo().DB_HOST,
            port=DBInfo().DB_PORT,
            user=DBInfo().DB_USER,
            passwd=DBInfo().DB_PASS,
            db=DBInfo().DB_NAME,
            # charset='utf-8'
        )

class DBInfo:
    def __init__(self):
        load_dotenv()
        self.DB_NAME = os.getenv('DB_NAME')
        self.DB_HOST = os.getenv('DB_HOST')
        self.DB_USER = os.getenv('DB_USER')
        self.DB_PASS = os.getenv('DB_PASS')
        self.DB_PORT = int(os.getenv('DB_PORT'))

