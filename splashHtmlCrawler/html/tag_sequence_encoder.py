import difflib

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
                               'input': 'h',
                               'form': 'i'}

    def path_generator(self):
        for main_dir, sub_dir_list, file_name_list in os.walk('./pms'):
            for file_name in file_name_list:
                yield [os.path.join(main_dir, file_name), file_name]  # 返回path与文件名组成的列表

    def get_tag_sequence(self, html):
        context = html.read()
        sequence = ''
        for tag in self.pattern.finditer(context):
            code = self.tag_white_dict.get(tag.group(1))
            if code is not None:
                sequence += code

        # print(sequence[:100])
        return sequence[:100]
        # return sequence

    def save_tag_sequence(self, domain, sequence):
        sql = 'insert into tag_domain("tag_sequence", "domain") values("%s","%s")' % (sequence, domain)
        self.cursor.execute(sql)
        self.conn.commit()


if __name__ == '__main__':
    encoder = Encoder()
    file_generator = encoder.path_generator()
    li = []
    while True:
        try:
            file = next(file_generator)
            file_path = file[0]
            file_name = file[1]
            with open(file_path, 'r', encoding='utf-8') as f:
                # print(file_name)
                li.append(encoder.get_tag_sequence(f))
                # encoder.save_tag_sequence(file_name, sequence)
        except StopIteration:
            print('All item processed')
            break
    with open('./test.txt', 'w+')as f:
        a = li[11]
        count = 1
        for b in li:

            f.write('\t'.join([str(difflib.SequenceMatcher(None, a, b).ratio()), str(count), a, b]) + '\n\n')
            count += 1
