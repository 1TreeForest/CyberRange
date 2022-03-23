import os, sys
from socket import gethostbyname

# DOMAIN= "G:/PycharmProject/fullstack2/week1/domain.txt"
import pymysql


def main():
    # domain.txt里面存储的是需要批量解析的域名列表，一行一个
    conn = pymysql.Connect(  # 配置数据库
        host='1.15.220.155',
        port=3306,
        user='test',
        password='991125',
        db='spider',
        charset='UTF8'
    )
    cursor = conn.cursor()
    sql = 'select domain from cluster where ipc is null'
    cursor.execute(sql)
    res = cursor.fetchall()
    for line in res:
        line = line[0]
        try:
            host = gethostbyname(line.strip('\n'))
        except Exception as e:
            print(e)
        else:
            sql2 = 'update cluster set ipc = %s, ipc_code = %s where domain = %s'
            ip = host.split('.')
            ipc = '{}.{}.{}'.format(ip[0], ip[1], ip[2])
            ipc_code = ''
            for i in ip[:-1]:
                while len(i) < 3:
                    i = '0' + i
                ipc_code += i
            print(ipc, ipc_code)
            cursor.execute(sql2, [ipc, ipc_code, line])
            conn.commit()
            # result.txt里面存储的是批量解析后的结果，不用提前创建
            # with open('result.txt', 'a+') as r:
            #     r.write(host + '\n')


if __name__ == '__main__':
    main()
