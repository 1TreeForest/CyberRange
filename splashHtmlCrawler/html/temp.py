import pymysql
import os

conn = pymysql.Connect(  # 配置数据库
    host='1.15.220.155',
    port=3306,
    user='test',
    password='991125',
    db='spider',
    charset='UTF8'
)

cursor = conn.cursor()

sql = 'select host from infrastructure'
sql2 = 'insert ignore into domain_homepage(domain) values(%s)'
cursor.execute(sql)

re = cursor.fetchall()
li = [str(i) for i in range(10)]
count = 0
for i in re:
    i = i[0]
    if i[-1] in li:
        continue
    else:
        cursor.execute(sql2, i)
        print(i )
        conn.commit()
