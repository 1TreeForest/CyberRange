import pymysql
import os
import re
import Levenshtein


class Similarity():
    pattern = None
    conn = None
    cursor = None
    item_dict = {}

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
        sql = 'SELECT domain, tag_sequence FROM `tag_domain`'
        # 执行
        self.cursor.execute(sql)
        self.item_dict = dict(self.cursor.fetchall()[:])
        domain_list = list(self.item_dict.keys())
        # print(domain_list)
        domain_list_len = len(domain_list)
        for i in range(domain_list_len):
            domain_1 = domain_list[i]
            sql = 'SELECT count(*) FROM `structure_similarity_500` where domain_1=%s'
            # 执行
            self.cursor.execute(sql, domain_1)
            exist_count = self.cursor.fetchone()[0]
            if exist_count == domain_list_len - i - 1:
                print(domain_1 + '已全部处理完毕，跳过')
                continue
            for domain_2 in domain_list[i + 1:]:
                # (sum-ldist)/sum, 其中sum是指str1和str2字串的长度总和，ldist是类编辑距离
                similarity = Levenshtein.ratio(self.item_dict[domain_1][:500], self.item_dict[domain_2][:500])
                print('\t'.join([domain_1, domain_2, str(similarity)]))
                # print('domain_1: ' + domain_1)
                # print('domain_2: ' + domain_2)
                # print('similarity: ' + str(similarity) + '\n')
                self.save_structure_similarity(domain_1, domain_2, similarity)

    def save_structure_similarity(self, domain_1, domain_2, similarity):
        sql = 'insert ignore into structure_similarity_500(domain_1, domain_2, similarity)values(%s,%s,%s) on duplicate key update similarity=%s'
        self.cursor.execute(sql, [domain_1, domain_2, similarity, similarity])
        self.conn.commit()


if __name__ == '__main__':
    similarity = Similarity()
    similarity.count_structure_similarity()
