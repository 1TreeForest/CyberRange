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
s = 'select ipc from cluster'
cursor.execute(s)
res = cursor.fetchall()
for i in res:
    n = ''
    ll = (i[0]).split('.')
    for j in ll:
        length = len(j)
        while(length<3):
            length += 1
            j = '0' + j
        n += j
    s = 'update cluster set ipc_code = %s where ipc = %s'
    cursor.execute(s,[n,i[0]])
    # n+=1
    conn.commit