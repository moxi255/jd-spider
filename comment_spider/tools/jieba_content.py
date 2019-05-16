#!/usr/bin/env python
# encoding: utf-8
'''
@author: taiyc
@file: jieba_content
@time: 2019/3/30 10:30
'''

import jieba

# 加载用户字典
jieba.load_userdict('tools\\user_words.txt')


# 获取stop_words字典
def get_stop_words():
    words = []
    with open('tools\stop_words.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            words.append(line.strip())
        return words


# 获取评论分词
def get_jieba_comment(string):
    result = jieba.cut(string)
    jieba_content = ''
    stop_words = get_stop_words()
    for x in result:
        if x not in stop_words:
            jieba_content += " " + x
    return jieba_content