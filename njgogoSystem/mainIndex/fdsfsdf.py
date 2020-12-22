import time
import datetime
import numpy as np
# a='2020-12-15'
# b='09:40'
# aa=datetime.datetime.strptime(b,"%H:%M")
# cc=aa+datetime.timedelta(minutes=15)*2
# ab=cc.strftime("%H:%M")
# print(datetime.timedelta(minutes=15)*2)

# time1= "2019-5-12 12:13:14"		# 字符串 日期
# d1 = time.strptime(str(time1),'%Y-%m-%d %H:%M:%S')
# print(type(d1))
# # d1=datetime.datetime.now()
# # print(type(d1))
# plus= d1 + timedelta(minutes=15)		# 加
# minus = d1 - timedelta(minutes=15)		# 减
# print(time1)
# print(d1)
# print(plus)
# print(minus )
a={'A':5,'B':4,'C':8}
b={'A':5,'B':2,'C':3}
#
import pandas as pd
# df=pd.DataFrame([a,b],index=['shengci','shengju'])
# print(df)
# df2=pd.DataFrame(df.values.T, index=df.columns, columns=df.index)
# print(df2)
# df3=df2.sort_values(axis=0,ascending=True,by=['shengci'])
# print(df3)
# print(df3.index.get_loc('A'))
# k=3
# n=2**k
# a=np.zeros((n,n))
# #
# a[0][0]=1
# a[1][1]=1
# a[1][0]=2
# a[0][1]=2
#
# for i in range(1,k):
#     half=2**i
#     # 左下角的子表中项为左上角子表对应项加2**i
#     for row in range(half):
#         for col in range(half):
#             a[row+half][col]=a[row][col]+half
#
#     # 右上角的子表等于左下角子表
#     for row in range(half):
#         for col in range(half):
#             a[row][col+half]=a[row+half][col]
#
#     # 右下角的子表等于左上角的子表
#     for row in range(half):
#         for col in range(half):
#             a[row+half][col+half]=a[row][col]
#
# print(a)

a=['g','h','d','t','u','p']
b=''
os=a
# for i in range(0,len(a),2):
#     t = []
#     t.append(a[i])
#     t.append(a[i+1])
#     os.append(t)
# o=os
# for i in range(len(a)-1):
#     hj=o[1][0]
#     for u in range(1,len(o)):
#         if u<(len(o)-1):
#             o[u][0]=o[u+1][0]
#         if u==(len(o)-1):
#             o[u][0]=o[u][1]
#     for u in range(1, len(o)):
#         o[len(o)-u][1]=o[len(o)-u-1][1]
#     o[0][1]=hj         for i in exp_fenzuqk:
#             all_fenzuqk.append(i.split('|')[1:-1])
#     for g in o:
#         print(g[0]+'VS'+g[1])
#
# print(a)
# a.append('rr')
# a.pop(0)
# os.append([x for x in a])
# print(os)
# import re
# a='sjf+sd+de.'
# b=re.findall(r'\+(.*)\.',a,re.I)[1]
# print(b)
if b:
    print('s')
else:
    print('r')