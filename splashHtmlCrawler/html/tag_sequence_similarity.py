import pymysql
import os
import re
import Levenshtein


class Similarity():
    pattern = None
    conn = None
    cursor = None
    item_dict = []

    def __init__(self):
        self.conn = pymysql.Connect(  # 配置数据库
            host='1.15.220.155',
            port=3306,
            user='test',
            password='991125',
            db='spider',
            charset='UTF8'
        )
        self.cursor = self.conn.cursor()

    def count_structure_similarity(self):
        sql = 'SELECT domain, tag_sequence FROM `tag_domain` '
        # 执行
        self.cursor.execute(sql)
        # 提交事务
        self.conn.commit()
        self.item_dict = dict(self.cursor.fetchall()[:])
        domain_list = list(self.item_dict.keys())
        print(domain_list)
        for i in range(len(domain_list)):
            domain_1 = domain_list[i]
            for domain_2 in domain_list[i+1:]:
                # 计算jaro距离
                similarity = Levenshtein.jaro(self.item_dict[domain_1][:500], self.item_dict[domain_2][:500])
                print('domain_1: ' + domain_1)
                print('domain_2: ' + domain_2)
                print('similarity: ' + str(similarity) + '\n')
                self.save_structure_similarity(domain_1, domain_2, similarity)

    def save_structure_similarity(self, domain_1, domain_2, similarity):
        sql = 'insert ignore into structure_similarity(domain_1, domain_2, similarity)values("%s","%s","%.2f")' % (
        domain_1, domain_2, similarity)
        self.cursor.execute(sql)
        self.conn.commit()


if __name__ == '__main__':
    similarity = Similarity()
    similarity.count_structure_similarity()
