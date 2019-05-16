#!/usr/bin/env python
# encoding: utf-8
'''
@author: taiyc
@file: comment_analysis
@time: 2019/4/2 21:00
'''

import pymysql
from judge_polarity import DictClassifier

class Analysis(object):
    def __init__(self):
        self.connect = None
        self.cursor = None
        self.score = 0
        self.total_score = 0

    def connect_sql(self):
        """
        连接数据库
        :return:
        """
        self.connect = pymysql.connect(
            host='localhost',
            port=3309,
            user='root',
            password='123456',
            db='jd_computer'
        )
        self.cursor = self.connect.cursor()

    def close_sql(self):
        """
        关闭数据库
        :return:
        """
        self.connect.commit()
        self.connect.close()
        self.cursor.close()

    def get_goods_id(self):
        """
        获取computer表中的computer_id
        :return:
        """
        self.connect_sql()
        sql = 'SELECT computer_id FROM computer'
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        self.close_sql()
        for goods_id in results:
            yield goods_id[0]

    def select_comment(self, computer_id):
        """
        查询评论表内所有computer_id的评论
        :param good_id:
        :return:
        """
        self.connect_sql()
        sql = f'SELECT content FROM computer_comment WHERE computer_id={computer_id}'
        self.cursor.execute(sql)
        # 取出goods_id的content结果集
        content_data = self.cursor.fetchall()
        # content数大于99条的进行数据分析
        # print(content_data)
        if len(content_data) > 99:
            self.close_sql()
            return content_data

        else:
            print(f'------{computer_id}评论不足,仅有{len(content_data)}------')
            del_tags_sql = f'DELETE FROM computer_tag WHERE computer_id={computer_id}'
            self.cursor.execute(del_tags_sql)
            print('删除便签成功')
            del_comment_sql = f'DELETE FROM computer_comment WHERE computer_id={computer_id}'
            self.cursor.execute(del_comment_sql)
            print('删除评论成功')
            del_computer_sql = f'DELETE FROM computer WHERE computer_id={computer_id}'
            self.cursor.execute(del_computer_sql)
            print(f'---------删除笔记本{computer_id}所有信息成功。---------')
            self.close_sql()
            return None
        # 小于则放弃分析
        # else:
        #     self.close_sql()
        #     return None


    def analysis_content(self, content):
        """
        分析评论获取评论情感好评率
        :param content:
        :return:
        """
        obj = DictClassifier()
        result = obj.analyse_sentence(content)
        print(f'{result}: {content}')
        self.total_score += result

    def save_result(self, goods_id, good_rate):
        """
        :param goods_id:
        :return:
        """
        print(good_rate)
        if int(good_rate) == 1:
            good_rate = 0.99
        self.connect_sql()
        print(f'{goods_id}评论情感分析好评率：{good_rate}')
        sql = f'UPDATE computer SET good_rate={good_rate} WHERE computer_id={goods_id}'
        self.cursor.execute(sql)
        self.close_sql()


if __name__ == '__main__':
    obj = Analysis()
    for good_id in obj.get_goods_id():
        content_data = obj.select_comment(good_id)
        # if content_data:
        #     total_num = len(content_data)
        #     obj.total_score = 0
        #     for content in content_data:
        #         content = content[0]
        #         obj.analysis_content(content)
        #     good_rate = round(obj.total_score / total_num, 4)
        #     obj.save_result(good_id, good_rate)
