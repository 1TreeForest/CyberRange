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

for maindir, subdir, file_name_list in os.walk(r'./homepage'):
    for file_name in file_name_list:
        file_path = './homepage/' + file_name
        if os.path.getsize(file_path) < 6144:
            print(file_name)
            sql = 'delete from pms where domain = "{0}"'
            cursor.execute(sql.format(file_name[:-5]))
            sql = 'delete from sites where domain = "{0}"'
            cursor.execute(sql.format(file_name[:-5]))
            sql = 'delete from domain_homepage where domain = "{0}"'
            cursor.execute(sql.format(file_name[:-5]))
            conn.commit()
            os.remove(file_path)

