import matplotlib.pyplot as plt
import numpy as np
import pymysql
#
# conn = pymysql.Connect(  # 配置数据库
#     host='1.15.220.155',
#     port=3306,
#     user='test',
#     password='991125',
#     db='spider',
#     charset='UTF8'
# )
#
# cursor = conn.cursor()
#
# count = {}
#
# sql2 = 'SELECT test_group,count(*) FROM `cluster` group by test_group'
# cursor.execute(sql2)
# res = cursor.fetchall()
# res_list = [i[1] for i in res]
#
# plt.hist(res_list, bins=30)

import numpy as np
from sklearn.cluster import *
from sklearn import metrics
from sklearn.preprocessing import StandardScaler, RobustScaler
import matplotlib.pyplot as plt
import pandas as pd
import sklearn.metrics as sm
import matplotlib.pyplot as plt
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

sql = 'select domain, test_layout_group, test_tfidf_group, app_group, ipc_code from cluster_noadj'
cursor.execute(sql)

dataset = cursor.fetchall()
temp_X = pd.DataFrame(dataset)
domains = temp_X[[0]]
X = temp_X[[1, 2, 3, 4]]
X = RobustScaler().fit_transform(X)
df = pd.DataFrame(X)
data = df[[3]]
plt.figure(figsize=[8,8])
plt.hist(data, bins=30)
plt.xlabel('value', fontsize=23)
plt.ylabel('count', fontsize=23)
plt.xticks(fontsize=20, rotation=45)
plt.yticks(fontsize=20)
plt.show()
