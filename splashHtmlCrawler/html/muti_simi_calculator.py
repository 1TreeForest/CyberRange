import time
import random

from multiprocessing import Process, Queue, current_process, freeze_support

import Levenshtein
import pymysql


def slave(task_queue, domain_list, item_dict, domain_list_len):
    conn = pymysql.Connect(  # 配置数据库
        host='1.15.220.155',
        port=3306,
        user='test',
        password='991125',
        db='spider',
        charset='UTF8'
    )
    cursor = conn.cursor()
    for task in iter(task_queue.get, 'STOP'):
        domain_1 = domain_list[task[0]]
        sql = 'SELECT count(*) FROM `structure_similarity_{0}` where domain_1=%s'.format(str(task[1]))
        # 执行
        cursor.execute(sql, domain_1)
        exist_count = cursor.fetchone()[0]
        if exist_count == domain_list_len - task[0] - 1:  # 对库中初始样本进行断点续连式对比，如果相等则证明该条已经和所有其他项目对比过了
            print('{0}:\t{1}\t{2}\t已全部处理完毕，跳过'.format(current_process().name, task[1], domain_1))
            continue
        for domain_2 in domain_list[task[0] + 1:]:
            # (sum-ldist)/sum, 其中sum是指str1和str2字串的长度总和，ldist是类编辑距离
            similarity = Levenshtein.ratio(item_dict[domain_1][:task[1]],
                                           item_dict[domain_2][:task[1]])  # task[1]是用户选择的tag长度
            print('\t'.join(['{0}:'.format(current_process().name), str(task[1]), domain_1, domain_2, str(similarity)]))
            sql = 'insert ignore into structure_similarity_{0}(domain_1, domain_2, similarity)values(%s,%s,%s) on duplicate key update similarity=%s'.format(
                task[1])
            cursor.execute(sql, [domain_1, domain_2, similarity, similarity])
            conn.commit()


def master():
    NUMBER_OF_PROCESSES = 50  # 最大进程数量
    task_queue = Queue()
    conn = pymysql.Connect(  # 配置数据库
        host='1.15.220.155',
        port=3306,
        user='test',
        password='991125',
        db='spider',
        charset='UTF8'
    )
    cursor = conn.cursor()
    sql = 'SELECT domain, tag_sequence FROM `tag_domain`'
    # 执行
    cursor.execute(sql)
    item_dict = dict(cursor.fetchall()[:])
    domain_list = list(item_dict.keys())
    domain_list_len = len(domain_list)

    for tag_len in [250, 500]:  # 对多长的tag进行对比
        for i in range(domain_list_len):
            task_queue.put([i, tag_len])

    #  give tasks
    for i in range(NUMBER_OF_PROCESSES):
        Process(target=slave, args=(task_queue, domain_list, item_dict, domain_list_len)).start()  # 创建进程，使用队列通信，共同完成队列中的任务
        print('{0} slaves is working'.format(NUMBER_OF_PROCESSES))

    # Tell child processes to stop
    for i in range(NUMBER_OF_PROCESSES):
        task_queue.put('STOP')


if __name__ == '__main__':
    freeze_support()
    master()
