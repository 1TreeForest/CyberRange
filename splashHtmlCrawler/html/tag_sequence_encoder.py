import Levenshtein
import pymysql
import os
import re


class Encoder():
    pattern = None
    conn = None
    cursor = None
    tag_white_dict = None

    def __init__(self):
        self.pattern = re.compile(r'</?(\w+).')
        self.conn = pymysql.Connect(  # 配置数据库
            host='1.15.220.155',
            port=3306,
            user='test',
            password='991125',
            db='spider',
            charset='UTF8'
        )
        self.cursor = self.conn.cursor()
        self.tag_white_dict = {'a': 'A', 'div': 'B', 'link': 'C', 'img': 'D', 'script': 'E', 'ul': 'F', 'li': 'G',
                               'input': 'H', 'form': 'I', 'p': 'J', 'table': 'K'}
        sql3 = 'SELECT domain, tag_sequence FROM `tag_domain_new`'
        # 执行
        self.cursor.execute(sql3)
        self.item_dict = dict(self.cursor.fetchall()[:])

    def path_generator(self):
        for main_dir, sub_dir_list, file_name_list in os.walk('./homepage'):
            for file_name in file_name_list:
                yield [os.path.join(main_dir, file_name), file_name]  # 返回path与文件名组成的列表

    def get_tag_sequence(self, html):
        count = 0
        context = html.read()
        sequence = ''
        for tag in self.pattern.finditer(context):
            code = self.tag_white_dict.get(tag.group(1))
            if code is not None:
                sequence += code
                count += 1
            if count >= 1000:
                break
        return sequence[:1000]

    def save_tag_sequence(self, domain, sequence):
        sql2 = 'insert ignore into tag_domain_new(tag_sequence, domain) values(%s,%s)'
        self.cursor.execute(sql2, [sequence, domain])
        self.conn.commit()

    def count_structure_similarity(self, domain_1, sequence):
        '''
        :param len_choose: the length you select to count and save
        :param domain_1: newly added domains
        :param sequence: tag sequence of domain_1
        :return: No return value, only similarity is stored to the database
        '''
        domain_list = list(self.item_dict.keys())
        # print(domain_list)
        for domain_2 in domain_list:
            # (sum-ldist)/sum, 其中sum是指str1和str2字串的长度总和，ldist是类编辑距离
            s1 = Levenshtein.ratio(sequence[:250], self.item_dict[domain_2][:250])
            s2 = Levenshtein.ratio(sequence[250:500], self.item_dict[domain_2][250:500])
            s3 = Levenshtein.ratio(sequence[500:750], self.item_dict[domain_2][500:750])
            s4 = Levenshtein.ratio(sequence[750:], self.item_dict[domain_2][750:])
            sql1 = 'insert ignore into structure_similarity_all(domain_1, domain_2, similarity_1, similarity_2, similarity_3, similarity_4)values(%s,%s,%s,%s,%s,%s)'
            try:
                self.cursor.execute(sql1, [domain_1, domain_2, s1, s2, s3, s4])
                self.conn.commit()
            except Exception as e:
                print(e)
            print('\t'.join([domain_1, domain_2, str(s1), str(s2), str(s3), str(s4)]))


if __name__ == '__main__':
    encoder = Encoder()
    file_generator = encoder.path_generator()
    sql = 'select domain from domain_homepage where isPMS = 1'
    encoder.cursor.execute(sql)
    pms = encoder.cursor.fetchall()
    print(pms)
    while True:
        try:
            file = next(file_generator)
            file_path = file[0]
            file_name = file[1]
            print((file_name[:-5],))
            if (file_name[:-5],) not in pms:  # 不是pms的网站不提取序列
                continue
            sql = 'SELECT count(*) FROM `tag_domain_new` where domain=%s'
            # 执行
            encoder.cursor.execute(sql, file_name[:-5])
            exist_count = encoder.cursor.fetchone()[0]
            if exist_count:  # 若已编码，则证明此文件已经处理过了，跳过
                continue
            with open(file_path, 'r', encoding='utf-8') as f:
                # print(file_name)
                sequence = encoder.get_tag_sequence(f)
                # encoder.count_structure_similarity(file_name[:-5], sequence)  # 直接对比的功能开关
                encoder.save_tag_sequence(file_name[:-5], sequence)  # 此文件已经对比完成，入库
        except StopIteration:
            print('All item processed')
            break
