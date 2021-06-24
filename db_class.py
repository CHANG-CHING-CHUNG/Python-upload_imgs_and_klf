import psycopg2 as pg2
import os
from dotenv import load_dotenv

load_dotenv()
class Database:
  def __init__(self, host, database, user, password):
    self.host = host
    self.database = database
    self.user = user
    self.password = password
    self.cur = None
    self.conn = None

  def connect(self):
    self.conn = pg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
    self.cur = self.conn.cursor()
    print('DB connected')
  def execute_query(self, query,var):
    self.cur.execute(query,var)
    self.conn.commit()

  def exceute_query_without_commit(self, query, var):
    self.cur.execute(query,var)

  def commit(self):
    self.conn.commit()

  def close(self):
    self.cur.close()
    self.conn.close()

  def fetchone(self):
    return self.cur.fetchone()

  def fetchall(self):
    return self.cur.fetchall()
  
  def Binary(self,data):
    return pg2.Binary(data)

host = os.getenv("DB_HOST")
database = os.getenv("DB_DATABASE")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

db = Database(
    host,
    database,
    user,
    password)


db.connect()