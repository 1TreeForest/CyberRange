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
        for domain1 in self.item_dict.keys():
            for domain2 in self.item_dict.keys():
                # 计算jaro距离
                similarity = Levenshtein.jaro(self.item_dict[domain1][:500], self.item_dict[domain2][:500])
                print('domain1: ' + domain1)
                print('domain2: ' + domain2)
                print('similarity: ' + str(similarity) + '\n')
                self.save_structure_similarity(domain1, domain2, similarity)


    def save_structure_similarity(self, domain1, domain2, similarity):
        sql = 'insert ignore into structure_similarity(domain_1, domain_2, similarity)values("%s","%s","%.4f")' % (domain1, domain2, similarity)
        self.cursor.execute(sql)
        self.conn.commit()


if __name__ == '__main__':
    similarity = Similarity()
    similarity.count_structure_similarity()