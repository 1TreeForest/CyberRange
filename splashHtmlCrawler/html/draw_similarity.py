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
sql = 'select similarity from structure_similarity_250'
cursor.execute(sql)
results = cursor.fetchall()

count = {}
for i in range(21):
    count[i] = 0

for i in results:
    v = float(i[0])
    count[int(v * 20)] += 1

xticks = [i for i in range(21)]

plt.bar(range(21), [count.get(xtick) for xtick in xticks], align='center', yerr=0.000001)
# 设置柱的文字说明
# 第一个参数为文字说明的横坐标
# 第二个参数为文字说明的内容
plt.xticks(range(21), xticks)

# 设置横坐标轴的标签说明
plt.xlabel('similarity')
# 设置纵坐标轴的标签说明
plt.ylabel('count')
# 设置标题
plt.title('count of each similarity')
# 绘图
plt.show()
