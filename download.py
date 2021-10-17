from WindPy import *
import pandas as pd
import pymysql
from sqlalchemy import create_engine
from tools import query

code_df = query('s_code') #读取数据库中的数据，返回为df格式
code_list=code_df['CODE'].values.tolist() #将df格式中的code列转化为列表
print(code_list)
w.start()
for code in code_list:
    a=w.wsd(code, "trade_code,sec_name,chg,pct_chg,industry_sw_2021", "2019-01-01", "2021-10-15", "industryType=1;PriceAdj=F") #从wind拉取数据，数据维度可以自由选择，date作为index
    # print(a)
    fm=pd.DataFrame(a.Data,index=a.Fields,columns=a.Times)  #将WindData的数据格式转化为dataframe
    fm=fm.T #转置
    # print(fm.head())
    # fm.to_csv('D:\\a.csv', sep=',', header=True, index=True, encoding = 'utf_8_sig') #

    # 构建导入引擎
    engine = create_engine('mysql+pymysql://root:yangming@localhost:3306/stock_data?charset=utf8')
    #  df是已有的Dataframe类型数据
    fm.to_sql('s_data', con=engine, index=True, if_exists='append')

