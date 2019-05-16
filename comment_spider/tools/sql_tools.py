#!/usr/bin/env python
# encoding: utf-8
'''
@author: taiyc
@file: sql_tools
@time: 2019/3/29 22:22
'''

import pymysql

def connect_mysql():
    """
    连接数据库
    :return: connect, cursor
    """
    connect = pymysql.Connect(host='localhost', user='root', password='123456', port=3309,
                              db='jd_computer'
                              )
    cursor = connect.cursor()
    return connect, cursor

def close_mysql(connect, cursor):
    """
    关闭数据库
    :param connect:
    :return:
    """
    connect.commit()
    cursor.close()
    connect.close()

# 获取start_urls
def get_start_urls():
    """
    获取start_urls
    :return:
    """
    connect, cursor = connect_mysql()
    select_sql = 'SELECT computer_id FROM computer WHERE if_spider=0'
    cursor.execute(select_sql)
    result = cursor.fetchall()
    close_mysql(connect, cursor)
    print(len(result))
    return [f'https://club.jd.com/comment/skuProductPageComments.action?&productId={url[0]}&score=0&sortType=5&page=1&pageSize=10&isShadowSku=0&rid=0&fold=1%27' for url in result]

# 保存标签
def save_tags(*args):
    """
    保存标签数据to computer_tag
    :param args:
    :return:
    """
    connect, cursor = connect_mysql()
    try:
        insert_sql = 'INSERT INTO computer_tag(tags, count, computer_id) VALUES (%s, %s, %s)'
        if_exists_sql = 'SELECT COUNT(*) FROM computer_tag WHERE computer_id={}'.format(args[2])
        cursor.execute(if_exists_sql)
        if not cursor.fetchall()[0][0]:
            cursor.execute(insert_sql, args)
            print(f'{args[2]}的评论标签数据添加成功。')
        else:
            print(f'{args[2]}的评论标签数据已存在！')
    except Exception as e:
        print(f'添加{args[2]}评论标签数据时数据库出现错误！！')
        print(e)
    finally:
        close_mysql(connect, cursor)

# 某个商品评论爬取完成将computer表 这个商品的if_spider设为1
def update_if_spider(computer_id):
    connect, cursor = connect_mysql()
    updata_sql = f'UPDATE computer SET if_spider=1 WHERE computer_id={computer_id}'
    cursor.execute(updata_sql)
    print(f'{computer_id} 评论爬取完成！')
    close_mysql(connect, cursor)

# 保存评论
def save_comment(*args):
    connect, cursor = connect_mysql()
    # if_exists_sql = 'SELECT COUNT(*) FROM computer_comment WHERE comment_id={}'.format(args[0])
    insert_sql = 'INSERT INTO computer_comment(comment_id, content, jieba_content, score, create_time, computer_id) VALUES (%s, %s,%s,%s,%s,%s)'
    # cursor.execute(if_exists_sql)
    # if cursor.fetchall()[0][0]:
    #     update_sql = 'UPDATE computer_comment SET content=%s,jieba_content=%s WHERE comment_id = %s'
    #     cursor.execute(update_sql, (args[1], args[2], args[0]))
    #     close_mysql(connect, cursor)
    #     print(f'{args[0]}评论已更新！')
    # else:
    cursor.execute(insert_sql, args)
    close_mysql(connect, cursor)
    print(f'{args[0]}评论添加成功！')

def get_exists_comments():
    connect, cursor = connect_mysql()
    select_sql = 'SELECT comment_id FROM computer_comment'
    cursor.execute(select_sql)
    exists_comments = cursor.fetchall()
    close_mysql(connect, cursor)
    return [x[0] for x in exists_comments]

