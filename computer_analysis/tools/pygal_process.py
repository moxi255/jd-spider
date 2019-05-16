#!/usr/bin/env python
# encoding: utf-8
'''
@author: taiyc
@file: pygal_process
@time: 2019/4/3 13:55
'''

import pygal, pymysql
from pygal.style import BlueStyle
from wordcloud import WordCloud


def connect_sql():
    connect = pymysql.connect(
        user='root',
        password='123456',
        host='localhost',
        port=3309,
        db='jd_computer'
    )
    cursor = connect.cursor()
    return connect, cursor


def close_sql(connect, cursor):
    connect.commit()
    cursor.close()
    connect.close()


def create_wordcloud(goods_id):
    """
    生成产品评论词云图
    :param goods_id:
    :return:
    """
    connect, cursor = connect_sql()
    sql = f'SELECT jieba_content FROM computer_comment WHERE computer_id={goods_id}'
    cursor.execute(sql)
    result = cursor.fetchall()
    close_sql(connect, cursor)
    # 评论数大于50才生成词云图
    if len(result) >= 50:
        jieba_str = ''.join([x[0] for x in result]).replace('  ', '').replace('\n', '')
        wc = WordCloud(width=500,
                       height=500,
                       background_color='white',  # 背景颜色
                       max_words=50,  # 最大词数
                       max_font_size=100,  # 显示字体的最大值
                       font_path='STXINGKA.TTF',
                       random_state=200,  # 为每个词返回一个PIL颜色
                       )
        wc.generate(jieba_str)
        wc.to_file(f'static\wordcloud\{goods_id}.png')
        return True
    else:
        return False


def create_pie(goods_id):
    """
    生成用户评分饼状图
    :param goods_id:
    :return:
    """
    pie_chart = pygal.Pie(style=BlueStyle)
    connect, cursor = connect_sql()
    sql = f'SELECT score,count(score) FROM computer_comment WHERE computer_id={goods_id} GROUP BY score'
    cursor.execute(sql)
    result = cursor.fetchall()
    close_sql(connect, cursor)
    total = sum([x[1] for x in result])
    if total >= 5:
        pie_chart.title = f'{total}位买家评分分析饼状图(%)'
        for score_group in result:
            pie_chart.add(str(score_group[0])+'分', round(score_group[1]/total, 4)*100)
        pie_chart.render_to_file(f'static\pie\{goods_id}.svg')
        return True
    else:
        return False


def create_bar(goods_id):
    """
    生成标签柱状图
    :param goods_id:
    :return:
    """
    bar_chart = pygal.HorizontalBar(style=BlueStyle)
    bar_chart.title = '标签分析条形图'
    connect, cursor = connect_sql()
    sql = f'SELECT tags,count FROM computer_tag WHERE computer_id={goods_id}'
    cursor.execute(sql)
    result = cursor.fetchall()
    close_sql(connect, cursor)
    # 判断是否存在标签
    if result:
        tags = result[0][0].split('|')
        count = result[0][1].split('|')
        for index in range(len(tags)):
            bar_chart.add(tags[index], int(count[index]))
        bar_chart.render_to_file(f'static\\bar\{goods_id}.svg')
        return True
        # 标签不小于3个的生成图
        # if len(tags) >= 3:
        #     for index in range(len(tags)):
        #         bar_chart.add(tags[index], int(count[index]))
        #     bar_chart.render_to_file(f'..\static\bar\{good_id}.svg')
        #     return 'success'
        # else:
        #     # 返回标签字典
        #     tags_dict = {}
        #     for index in range(len(tags)):
        #         tags_dict[tags[index]] = count[index]
        #     print(tags_dict)
        #     return tags_dict
    else:
        return False


def jieba_top10_bar(goods_id):
    bar_chart = pygal.Bar(style=BlueStyle)
    bar_chart.title = '分词比重top10'
    connect, cursor = connect_sql()
    sql = f'SELECT jieba_content FROM computer_comment WHERE computer_id={goods_id}'
    cursor.execute(sql)
    result = cursor.fetchall()
    close_sql(connect, cursor)
    # 评论数大于50才生成
    if len(result) > 50:
        jieba_list = ''.join([x[0] for x in result]).replace('  ', '').replace('\n', '').split(' ')
        topn_dict = {}
        for word in jieba_list:
            if word:
                if word not in topn_dict:
                    topn_dict[word] = 1
                else:
                    topn_dict[word] = topn_dict[word] + 1
        stop = ['物流', '运行', '电脑', '客服', '收到', '开机', '东西', '质量', '购物']
        for s in stop:
            if s in topn_dict:
                topn_dict.pop(s)
        top10_list = sorted(topn_dict.items(), key=lambda item: item[1], reverse=True)[1:11]
        for heat_word in top10_list:
            bar_chart.add(heat_word[0], int(heat_word[1]))
        bar_chart.render_to_file(f'static\jieba_top10_bar\{goods_id}.svg')
        return True
    else:
        return False



# create_bar(6099496)
# print(create_bar(6099496))
# jieba_top10_bar(29196113704)
