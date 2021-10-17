from sqlalchemy import create_engine
import pandas as pd

#从书库中读取股票代码列表
# engine = create_engine('mysql+pymysql://root:yangming@localhost:3306/stock_data?charset=utf8')
# sql = 'select * from s_code'
# df1=pd.read_sql(sql,engine)
# print(type(df1))

def query(table):#定义一个函数用来专门从数据库中读取数据
    host='localhost'
    user='root'
    password='yangming'
    database='stock_data'
    port=3306
    conn=create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(user,password,host,port,database))
    sql='select * from '+str(table) + ' where 1=1 limit 1'
    results=pd.read_sql(sql,conn)
    return results