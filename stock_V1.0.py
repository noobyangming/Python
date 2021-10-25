import pandas as pd
from sqlalchemy import create_engine
from openpyxl import load_workbook
import pymysql

'''将excel中的数据读取，并写入mysql的表中'''
# df=pd.read_excel('stock_all.xlsx','Sheet1')
# temp_df = df[:][["简称","日期","涨跌(元)","涨跌幅","总市值(元)","市盈率"]]
# # 构建导入引擎
# engine = create_engine('mysql+pymysql://root:yangming@localhost:3306/stock?charset=utf8')
# #  df是已有的Dataframe类型数据
# temp_df.to_sql('s_data', con=engine, index=False, if_exists='replace')


'''此代码用于从wind数据库拉出数据，并存入数据库sql，或者csv文件'''
# from WindPy import *
# import pandas as pd
#
# w.start()
# code_list = ["000552.SZ","000571.SZ"]
# a=w.wsd("000552.SZ", "trade_code,sec_name,chg,pct_chg,industry_sw_2021", "2019-01-01", "2021-10-15", "industryType=1;PriceAdj=F") #从wind拉取数据，数据维度可以自由选择，date作为index
# fm=pd.DataFrame(a.Data,index=a.Fields,columns=a.Times)  #将WindData的数据格式转化为dataframe
# fm=fm.T #转置
# # 数据存到数据库
# engine = create_engine('mysql+pymysql://root:yangming@localhost:3306/stock_data?charset=utf8')  # 构建导入引擎
# con = engine.connect()
# fm.to_sql('s_data', con=engine, index=True, if_exists='append') # 数据导入sql数据库


'''此代码用于从mysql中读取数据，导出分析数据时需要；导出目标stock时也需要'''
con = pymysql.connect(host='localhost',user='root',password='yangming',database='stock_data',port=3306) #数据链接
sql = 'select * from s_data' #sql查询语句
df_sql=pd.read_sql(sql, con)    #调取数据库数据
df_source = df_sql.dropna(axis=0, how='any') #去除含有空置的列
# df_source = df_source.reset_index(drop=True)  #重构索引，从0开始，不想保留原来的index，使用参数 drop=True，默认 False。
# print(df_source.head())

# #通过wind导出的数据进行stock量化分析，用于导出分析样本数据
# sdate = ['2019-01-01 0:0:0', '2020-01-01 0:0:0', '2021-01-01 0:0:0', '2022-01-01 0:0:0']
# # sdate = ['2020-01-01 0:0:0', '2021-01-01 0:0:0']
# sn_list = list(df_source.drop_duplicates(subset=['简称'], keep='first', inplace=False).简称)
# drop_times = 4
# df_output = pd.DataFrame(columns=["简称", "下跌4次后上涨", "下跌4次", "比率", "统计起期"])
# for a in range(3):
#     for sn in sn_list:
#         df_stock = df_source[(df_source["简称"] == sn)&(df_source['日期'] > sdate[a])&(df_source['日期'] < sdate[a+1])][['简称','日期','涨跌幅','行业分类']] #多条件筛选+列表筛选连用
#         df_stock = df_stock.reset_index(drop=True)  #重构索引
#         df_stock = df_stock.fillna(value=0)    #空值填充为0
#         sample_num = 0.0001  # 样本数量归零
#         bingo_num = 0  # 命中数量归零
#         # try:
#         #     category = df_stock.行业分类[0] #传递行业分类
#         # except: #防止取到空值而报错，有些stock是到2021年上市，之前没有数据
#         #     pass
#         # print(category)
#         for n in range(df_stock.shape[0]-drop_times):   #返回dataframe行列，shape[0]=rows,shape[1]=columns
#             '''针对每只股票数据进行量化处理'''
#             for i in range(drop_times):
#                 if df_stock.涨跌幅[n+i]>=0:
#                     break
#                 if i == (drop_times-1):
#                     sample_num += 1
#                     # print(df_stock.涨跌幅[n+i])
#                     if df_stock.涨跌幅[n+drop_times]>=0:
#                         bingo_num += 1
#                         # print(df_stock.涨跌幅[n+drop_times])
#         # print(sn,int(sample_num),bingo_num,bingo_num/sample_num)
#         df_output = df_output.append(pd.DataFrame({"简称":[sn], "下跌4次后上涨":[int(sample_num)], "下跌4次":[bingo_num], "比率":[bingo_num/sample_num], "统计起期":[sdate[a]]}),ignore_index=True)
# # print((df_output))
# book = load_workbook('output.xlsx')
# writer = pd.ExcelWriter('output.xlsx', engine='openpyxl')
# writer.book = book
# writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
# df_output.to_excel(writer, sheet_name="4次", encoding='utf-8', index=False, header=True)
# writer.save()


# '''将excel中的数据读取，并写入mysql的表中，写入经过分析后，缩小范围后的stock代码'''
# df=pd.read_excel('output_a.xlsx','Sheet1')
# # temp_df = df[:][["简称","日期","涨跌(元)","涨跌幅","总市值(元)","市盈率"]]
# # 构建导入引擎
# engine = create_engine('mysql+pymysql://root:yangming@localhost:3306/stock_data?charset=utf8')
# #  df是已有的Dataframe类型数据
# df.to_sql('t_code', con=engine, index=False, if_exists='replace')




'''筛选最近连续跌了3天的股票，导出目标stock'''
#读取目标股票简称
con = pymysql.connect(host='localhost',user='root',password='yangming',database='stock_data',port=3306) #数据链接
sql = 'select * from t_code' #sql查询语句
df_code=pd.read_sql(sql, con)    #调取数据库数据
t_list = df_code.简称.tolist()    #df转化位list
forecast = 3
target_stock = []
for t in t_list:
    df_tstock = df_source[(df_source["简称"] == t)][['简称','代码','日期','涨跌幅']]
    df_tstock = df_tstock.sort_values("日期",inplace=False)
    df_tstock = df_tstock.tail(3)
    t_three = df_tstock.涨跌幅.tolist()
    # print(t_three)
    for f in range(forecast): #连续三条下跌
        if t_three[f] >= 0:
            break
        if f == (forecast-1):
            target_stock.append(t)
df_target_stock = pd.DataFrame(target_stock, columns=["简称"]) #list转为df
df_target_stock.to_excel("output_target.xlsx",index=False) #存入excel
# print(target_stock)