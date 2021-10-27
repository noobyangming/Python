"""希望十字星model"""
import pandas as pd
from sqlalchemy import create_engine
from openpyxl import load_workbook
import pymysql
import model

'''此代码用于从mysql中读取数据，导出分析数据时需要；导出目标stock时也需要'''
con = pymysql.connect(host='localhost',user='root',password='yangming',database='stock_data',port=3306) #数据链接
sql = 'select * from s_data' #sql查询语句
df_sql=pd.read_sql(sql, con)    #调取数据库数据
df_source = df_sql.dropna(axis=0, how='any') #去除含有空置的列

#   单独举一个保险例子
# sn = '北大荒'
# df_stock = df_source[(df_source["简称"] == sn)] #多条件筛选+列表筛选连用
# df_stock = df_stock.fillna(value=0)    #空值填充为0


sn_list = list(df_source.drop_duplicates(subset=['简称'], keep='first', inplace=False).简称)  #列出stock清单名称
print(sn_list)

# """希望十字特征，下跌途中"""
# for sn in sn_list:
#     df_stock = df_source[(df_source["简称"] == sn)]  # 多条件筛选+列表筛选连用
#     df_stock = df_stock.sort_values(by="日期",ascending=True)
#     df_stock = df_stock.tail(20)
#     df_stock = df_stock.reset_index(drop=True)  # 重构索引
#     i = 0
#     for i in range(df_stock.shape[0]-2):
#         if model.big_down(df_stock,i): #大阴柱判断
#             # print(df_stock['简称'][i],df_stock['日期'][i],a,b,c)
#             if model.cross(df_stock,i+1):   #十字判单
#                 # print(df_stock['日期'][i+1], a1)
#                 if model.big_up(df_stock,i+2):  #大阳柱判断
#                     print(df_stock['简称'][i+2],df_stock['日期'][i+2])


# """希望之星特征，下跌途中"""
# for sn in sn_list:
#     df_stock = df_source[(df_source["简称"] == sn)]  # 多条件筛选+列表筛选连用
#     df_stock = df_stock.sort_values(by="日期",ascending=True)
#     df_stock = df_stock.tail(10)
#     df_stock = df_stock.reset_index(drop=True)  # 重构索引
#     i = 0
#     for i in range(df_stock.shape[0]-2):
#         if model.big_down(df_stock,i): #大阴柱判断
#             # print(df_stock['简称'][i],df_stock['日期'][i],a,b,c)
#             if model.small_updown(df_stock,i+1):   #小阴阳判断
#                 # print(df_stock['日期'][i+1], a1)
#                 if model.big_up(df_stock,i+2):  #大阳柱判断
#                     print(df_stock['简称'][i+2],df_stock['日期'][i+2])


"""曙光出现+旭日东升，下跌途中"""
for sn in sn_list:
    df_stock = df_source[(df_source["简称"] == sn)]  # 多条件筛选+列表筛选连用
    df_stock = df_stock.sort_values(by="日期",ascending=True)
    df_stock = df_stock.tail(3)
    df_stock = df_stock.reset_index(drop=True)  # 重构索引
    i = 0
    for i in range(df_stock.shape[0]-1):
        if model.big_down(df_stock,i): #大阴柱判断
            if model.down_up_half(df_stock,i): #判断阳柱是否插入阴柱二分之一
                if model.big_up(df_stock,i+1):  #大阳柱判断
                    print(df_stock['简称'][i+1],df_stock['日期'][i+1])
