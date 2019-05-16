# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class ComputerSpiderPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host='localhost',
            port=3309,
            user='root',
            password='123456',
            db='jd_computer'
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        sql = 'INSERT INTO computer(computer_id, brand, title, price, img_url, param) values (%s, %s, %s, %s, %s, %s)'
        if_exists_sql = f'SELECT count(*) FROM computer WHERE computer_id={item["goods_id"]}'
        self.cursor.execute(if_exists_sql)
        if self.cursor.fetchall()[0][0]:
            print(f'{item["goods_id"]}已存在')
            print(item['price'])
        elif round(float(item['price']), 2) < 1000:
            print(f'价格获取有误！放弃收集该产品！')
        else:
            self.cursor.execute(sql, (
                item['goods_id'], item['brand'], item['title'], item['price'], item['img_url'], item['param']))
            self.connect.commit()
            print(f'{item["goods_id"]}入库成功。')
            return item
