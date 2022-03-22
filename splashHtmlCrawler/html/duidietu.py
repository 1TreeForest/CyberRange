import pandas as pd
import matplotlib.pyplot as plt
import pymysql
import csv

# conn = pymysql.Connect(  # 配置数据库
#     host='1.15.220.155',
#     port=3306,
#     user='test',
#     password='991125',
#     db='spider',
#     charset='UTF8'
# )

# cursor = conn.cursor()
# sql = 'select similarity_1,similarity_2,similarity_3,similarity_4 from structure_similarity_all'
# cursor.execute(sql)
# results = cursor.fetchall()
#
# with open("draw.csv", "w") as csvFile:
#     reader = csv.reader(csvFile)
#     writer = csv.writer(csvFile)
#     fileHeader = ["segment", "count"]
#     count = {'0-250': 0,
#              '250-500': 0,
#              '500-750': 0,
#              '750-1000': 0}
#     for i in range(4):
#         count_interval = []
#         for k in range(50):
#             count_interval.append(0)
#         for j in results:
#             try:
#                 count_interval[int(j[i]*50)] += 1
#             except:
#                 count_interval[49] += 1
#         count['{0}-{1}'.format(i * 250, i * 250 + 250)] = count_interval
#
#     writer.writerow(fileHeader)
#
#     for key, value in count.items():
#         writer.writerow([key, value])
data = []
with open("draw.csv", "r") as f:
    for i in range(4):
        li = list(str(f.readline()).split(','))
        lj = []
        for item in li:
            lj.append(int(item))
        data.append(lj)
print(data)

# plt.ylabel(u'Number of Similarities within the Interval')  # 设置y轴，并设定字号大小
width_val = 0.8
# plt.figure(figsize=(12.80, 9.60))  # 设置画布的尺寸
# 通过bottom使得两个柱状图堆叠显示，且没有交叉
# alpha：透明度；width：柱子的宽度；facecolor：柱子填充色；edgecolor：柱子轮廓色；lw：柱子轮廓的宽度；label：图例；
# xs = [i for i in range(50)]
# plt.bar(xs, data[0][:], width=width_val, alpha=1, label='0-250', facecolor='#222222')
# plt.bar(xs, data[1][:], width=width_val, alpha=1, label='250-500', facecolor='#777777')
# plt.bar(xs, data[2][:], width=width_val, alpha=1, label='500-750', facecolor='#777777')
# plt.bar(xs, data[3][:], width=width_val, alpha=1, label='750-1000', facecolor='#cfcfcf')
#
#
x = range(50)
width = 1
# 将bottom_y元素都初始化为0
bottom_y = [0] * 50
labels = ['0-250', '250-500', '500-750', '750-1000']
colors = ['#cfcfcf', '#aaaaaa', '#777777', '#222222']
i = 0
for y in data:
    plt.bar(x, y, width, bottom=bottom_y, label=labels[i], facecolor=colors[i])
    i += 1
    # 累加数据计算新的bottom_y
    bottom_y = [a + b for a, b in zip(y, bottom_y)]

plt.legend(loc=1)  # 图例展示位置，数字代表第几象限
xalas = [i / 10 for i in range(11)]
plt.xticks([i * 5 - 0.5 for i in range(11)], xalas)
# plt.xticks(fontsize=18)
# plt.yticks(fontsize=18)
# plt.ylim((0, 250000))

plt.show()  # 显示图像
