import matplotlib.pyplot as plt
import numpy as np
import pymysql

conn = pymysql.Connect(  # 配置数据库
    host='1.15.220.155',
    port=3306,
    user='test',
    password='991125',
    db='spider',
    charset='UTF8'
)

cursor = conn.cursor()

count = {}

sql2 = 'SELECT group_tag,count(*) FROM `structure_group_test` group by group_tag order by count(*) desc limit 30'
cursor.execute(sql2)
res = cursor.fetchall()
res_list = [i[1] for i in res]
xticks = [i for i in range(30)]

plt.bar(range(30), res_list, align='center', yerr=0.000001)

xalas = []
for i in range(30):
    xalas.append('Group {0}'.format(i))
plt.xticks([i for i in range(30)], xalas)
plt.xticks(rotation=90)
plt.show()
