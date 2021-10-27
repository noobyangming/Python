# 特征模型

"""大阴柱模型"""
def big_down(df,i):
    v1 = 0.99  # 判断接近参数
    v2 = -3
    a = df['开盘价(元)'][i] / df['最高价(元)'][i]
    b = df['收盘价(元)'][i] / df['最低价(元)'][i]
    c = (df['收盘价(元)'][i] - df['开盘价(元)'][i]) / df['前收盘价(元)'][i] * 100  # 实体高度
    if a > v1 and b > v1 and c < v2:
        return(True)
        # print(df_stock['简称'][i],df_stock['日期'][i],a,b,c)

"""十字模型"""
def cross(df,i):
    v1 = 1.001   #判单接近参数
    v2 = 0.999
    a = df['开盘价(元)'][i]/df['收盘价(元)'][i]
    if a < v1 and a > v2:
        return (True)
        # print(df['日期'][i], a)

"""大阳柱模型"""
def big_up(df,i):
    v1 = 0.99 #判断接近参数
    v2 = 3
    a = df['收盘价(元)'][i]/df['最高价(元)'][i]
    b = df['开盘价(元)'][i]/df['最低价(元)'][i]
    c = (df['收盘价(元)'][i]-df['开盘价(元)'][i])/df['前收盘价(元)'][i]*100 #实体高度
    if a > v1 and b > v1 and c > v2:
        return (True)
        # print(df['日期'][i],a,b,c)

"""小阴阳模型"""
def small_updown(df,i):
    v1 = 1.005   #判单接近参数
    v2 = 0.995
    a = df['开盘价(元)'][i]/df['收盘价(元)'][i]
    if a < v1 and a > v2:
        return (True)
        # print(df['日期'][i], a)

"""曙光出现-判断阳柱插入阴柱1/2"""
def down_up_half(df,i):
    a = (df['收盘价(元)'][i]+df['开盘价(元)'][i])*0.5
    b = df['收盘价(元)'][i+1]
    if a < b:
        return (True)
        # print(df['日期'][i],a,b,c)

