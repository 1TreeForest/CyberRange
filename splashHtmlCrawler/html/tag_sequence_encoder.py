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
        self.tag_white_dict = {'a': 'a', 'div': 'b', 'link': 'c', 'img': 'd', 'script': 'e', 'ul': 'f', 'li': 'g',
                               'input': 'h', 'form': 'i', 'pre': 'j', 'noscript': 'k'}

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
        print(count)
        return sequence[:1000]

    def save_tag_sequence(self, domain, sequence):
        sql = 'insert ignore into tag_domain(tag_sequence, domain) values(%s,%s) on duplicate key update tag_sequence=%s'
        self.cursor.execute(sql, [sequence, domain, sequence])
        self.conn.commit()

    def count_structure_similarity(self, len_choose, domain_1, sequence):
        '''

        :param len_choose: the length you select to count and save
        :param domain_1: newly added domains
        :param sequence: tag sequence of domain_1
        :return: No return value, only similarity is stored to the database
        '''
        sql = 'SELECT domain, tag_sequence FROM `tag_domain`'
        # 执行
        self.cursor.execute(sql)
        self.item_dict = dict(self.cursor.fetchall()[:])
        domain_list = list(self.item_dict.keys())
        # print(domain_list)
        for domain_2 in domain_list:
            # (sum-ldist)/sum, 其中sum是指str1和str2字串的长度总和，ldist是类编辑距离
            similarity = Levenshtein.ratio(sequence[:len_choose], self.item_dict[domain_2][:len_choose])
            print('\t'.join([domain_1, domain_2, str(similarity)]))
            self.save_structure_similarity(domain_1, domain_2, similarity, len_choose)

    def save_structure_similarity(self, domain_1, domain_2, similarity, len_choose):
        sql = 'insert ignore into structure_similarity_{0}(domain_1, domain_2, similarity)values(%s,%s,%s) on duplicate key update similarity=%s'.format(len_choose)
        self.cursor.execute(sql, [domain_1, domain_2, similarity, similarity])
        self.conn.commit()

if __name__ == '__main__':
    encoder = Encoder()
    file_generator = encoder.path_generator()
    while True:
        try:
            file = next(file_generator)
            file_path = file[0]
            file_name = file[1]
            sql = 'SELECT count(*) FROM `domain_tag` where domain=%s'
            # 执行
            encoder.cursor.execute(sql, file_name[:-5])
            exist_count = encoder.cursor.fetchone()[0]
            if exist_count:  # 若已编码，则证明此文件已经处理过了，跳过
                continue
            with open(file_path, 'r', encoding='utf-8') as f:
                # print(file_name)
                sequence = encoder.get_tag_sequence(f)
                for len_choose in [250, 500, 750, 1000]:  # 计算四种长度的与已存在条目的相似度
                    encoder.count_structure_similarity(len_choose, file_name[:-5], sequence)  # 直接对比的功能开关
                encoder.save_tag_sequence(file_name[:-5], sequence)  # 此文件已经对比完成，入库
        except StopIteration:
            print('All item processed')
            break