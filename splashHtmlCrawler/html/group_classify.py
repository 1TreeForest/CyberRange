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
sql_1 = 'select distinct domain_1 from structure_similarity'
sql_2 = 'select domain_2 from structure_similarity where domain_1 = %s and similarity >= 0.9'
sql_3 = 'insert ignore into `structure_group` values(%s, %s)'
cursor.execute(sql_1)
domain_list = cursor.fetchall()
domain_list = list(i[0] for i in domain_list)
group = 0
for item in domain_list:
    cursor.execute(sql_2, item)
    results_2 = cursor.fetchall()
    if len(results_2) == 0:
        continue
    for i in results_2:
        cursor.execute(sql_3, [group, i[0]])
        try:
            domain_list.remove(i[0])
        except:
            continue
    cursor.execute(sql_3, [group, item])
    group += 1
    conn.commit()
