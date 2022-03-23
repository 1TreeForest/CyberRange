import time
from multiprocessing import Process, Queue, current_process, freeze_support, Manager

import Levenshtein
import pymysql


def slave(task_queue, group, count, grouped_item_dict, domain_list, item_dict, domain_list_len):
    conn = pymysql.Connect(  # 配置数据库
        host='1.15.220.155',
        port=3306,
        user='test',
        password='991125',
        db='spider',
        charset='UTF8'
    )
    cursor = conn.cursor()
    sql_check = 'select count(title_group) from cluster where domain = %s'
    for task in iter(task_queue.get, 'STOP'):
        domain_1 = domain_list[task[0]]
        cursor.execute(sql_check, domain_1)
        exist = (cursor.fetchone())[0]
        if exist:  # 断点重连
            continue
        if domain_1 in grouped_item_dict.keys():  # 已经被分组的项目不再计算，不给第二次机会
            continue
        for domain_2 in domain_list[task[0] + 1:]:
            similarity = Levenshtein.ratio(item_dict.get(domain_1), item_dict.get(domain_2))
            print(item_dict.get(domain_1), item_dict.get(domain_2), similarity)
            count.value += 1
            print('{0}:  {1}'.format(current_process().name, count.value))
            if similarity >= 0.9:
                exist_group = grouped_item_dict.get(domain_1)
                if exist_group is not None:
                    sql = 'update cluster set title_group = %s where domain = %s'
                    cursor.execute(sql, [exist_group, domain_2])
                    grouped_item_dict[domain_2] = exist_group
                else:
                    group_num = group.value
                    group.value += 1
                    grouped_item_dict[domain_1] = group_num
                    grouped_item_dict[domain_2] = group_num
                    sql = 'update cluster set title_group = %s where domain = %s'
                    cursor.execute(sql, [group_num, domain_1])
                    sql = 'update cluster set title_group = %s where domain = %s'
                    cursor.execute(sql, [group_num, domain_2])
                conn.commit()


def master():
    NUMBER_OF_PROCESSES = 20  # 最大进程数量
    mgr = Manager()
    task_queue = Queue()
    count = mgr.Value(int, 0)
    grouped_item_dict = mgr.dict()
    group = mgr.Value(int, 0)
    conn = pymysql.Connect(  # 配置数据库
        host='1.15.220.155',
        port=3306,
        user='test',
        password='991125',
        db='spider',
        charset='UTF8'
    )
    cursor = conn.cursor()
    sql = 'SELECT domain, title FROM `cluster`'
    # 执行
    cursor.execute(sql)
    item_dict = dict(cursor.fetchall()[:])
    domain_list = list(item_dict.keys())
    domain_list_len = len(domain_list)

    for tag_len in [1000]:  # 对多长的tag进行对比
        for i in range(domain_list_len):
            task_queue.put([i, tag_len])

    #  give tasks
    proc_list = []
    time_start = time.time()
    for i in range(NUMBER_OF_PROCESSES):
        p = Process(target=slave,
                    args=(task_queue, group, count, grouped_item_dict, domain_list, item_dict,
                          domain_list_len))  # 创建进程，使用队列通信，共同完成队列中的任务
        p.start()
        proc_list.append(p)
        time.sleep(2)
    print('{0} slaves are working'.format(NUMBER_OF_PROCESSES))

    # Tell child processes to stop
    for i in range(NUMBER_OF_PROCESSES):
        task_queue.put('STOP')

    for p in proc_list:
        p.join()
    time_end = time.time()
    print('time cost', time_end - time_start, 's')


if __name__ == '__main__':
    freeze_support()
    master()
