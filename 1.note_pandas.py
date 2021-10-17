import pandas as pd

df_source=pd.read_excel('stock_all.xlsx',header=0,sheet_name='Sheet1',skipfooter=0)  #目标表格数据, shipfooter是删除末尾*行的意思

'''pandas数据帅选规则'''
# x=df_source[df_source["前收盘价(元)"] > 220]   #筛选df_source对象中属性为"前收盘价(元)"大于220的所有数据
# x=df_source[df_source["简称"] == '有友食品']  #筛选df_source对象中属性为"简称"为有友食品的所有数据
# x=df_source[df_source['日期'] > '2021-8-11 0:0:0']    #筛选df_source对象中属性为"日期2021-8-11"大于的所有数据
# x=df_source[['日期','市盈率']]   #筛选指定列的DataFrame，直接传递数组给给DataFrame
# x=df_source['日期']   #获取一列Series
# x=df_source.drop('日期',axis=1) #drop方法，axis为0代表行，1代表列；行用数字表示
# x=df_source.groupby('简称')   #用groupby对其进行分组，对每个分组可以使用apply函数进行再处理（https://zhuanlan.zhihu.com/p/101284491）。注意groupby生成的是DataFrameGroupBy对象。
# list(x)   #可以对DataFrame文件进行列表处理，便于打印
# condition = df_source["简称"].str.startswith("有友")    #用于生成筛选条件。比如以"有友"开头的，如有友XX，有友XXXX都会被筛出来
# x=df_source[condition]
# x.head() #用于读取前*条数据， head(10)表示前10条，默认是5条。用户测试函数的速度
# x=df_source.sort_values(by='前收盘价(元)',ascending=False) #排序操作
# x=df_source.T #数据表反转dataframe-T
# x=df_source.日期[2] #用类似类+列表的方式选取数据
# x=list(df_source.drop_duplicates(subset=['简称'],keep='first',inplace=False).简称)  #针对"简称"列进行去重，并将获得的列转为一个数组
# x=df_source[(df_source["简称"] == '有友食品')&(df_source['日期'] > '2019-5-15 0:0:0')]  #多条件筛选
# print(x)


'''windpy包的使用''' #https://www.windquant.com/qntcloud/apiRefHelp/id-b89ae6bf-17db-40d6-8f7c-123702a30755
# from WindPy import * #pycharm安装时一定需要将WindPy.pth(可以自己建立，里面存放路径D:\Program Files\wind\x64)放入到项目目录下面(如D:\Python\Program\venv\Lib\site-packages)
# w.start() #启动windpy
# a=w.wsd("000001.SZ", "low,close", "2021-09-17", "2021-10-16", "") #拉取wind数据第一个为Codes，第二个为Fields，第三和第四个为Times的起止时间
# fm=pd.DataFrame(a.Data,index=a.Fields,columns=a.Times)    #将winddata转化为dataframe，注意此时的数据还是为转置的
# fm=fm.T #转置，获得最终需要的dataframe数据


'''此文件用于链接mysql数据库'''
import pymysql
#创建数据库链接，注意再创建数据库的时候格式选择utf-8，否则后面建表的时候会出错
con = pymysql.connect(host='localhost',user='root',password='yangming',database='stock_data',port=3306)
cur = con.cursor()
sql = """
    create table s_data(
    id int primary key auto_increment,
    s_code varchar(30) not null,
    chg float(3,1),
    pct_chg float(3,1),
    industry_sw_2021 varchar(30) not null
    ) 
"""
try:
    # 执行创建表的sql
    cur.execute(sql)
    print("创建表成功")
except Exception as e:
    print("创建表失败")
    print(e)
finally:
    # 关闭连接
    con.close()
    
    
'''此文件用于从wind数据库拉出数据，并存入数据库sql，或者csv文件''' 
from WindPy import *
import pandas as pd
from sqlalchemy import create_engine

w.start()
code_list = ["000552.SZ","000571.SZ"]
a=w.wsd("000552.SZ", "trade_code,sec_name,chg,pct_chg,industry_sw_2021", "2019-01-01", "2021-10-15", "industryType=1;PriceAdj=F") #从wind拉取数据，数据维度可以自由选择，date作为index
fm=pd.DataFrame(a.Data,index=a.Fields,columns=a.Times)  #将WindData的数据格式转化为dataframe
fm=fm.T #转置
# print(fm.head())

# 数据存入csv文件
# fm.to_csv('D:\\a.csv', sep=',', header=True, index=True, encoding = 'utf_8_sig') 

# 数据存到数据库
engine = create_engine('mysql+pymysql://root:yangming@localhost:3306/stock_data?charset=utf8')  # 构建导入引擎
con = engine.connect()
fm.to_sql('s_data', con=engine, index=True, if_exists='append') # 数据导入sql数据库
