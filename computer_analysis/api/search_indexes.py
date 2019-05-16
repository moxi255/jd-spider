#!/usr/bin/env python
# encoding: utf-8
'''
@author: taiyc
@file: search_indexes
@time: 2019/4/3 13:40
'''
from haystack import indexes
from api.models import Computer


class GoodsInfoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    good_rate = indexes.FloatField(model_attr='good_rate')
    computer_id = indexes.CharField(model_attr='computer_id')
    price = indexes.CharField(model_attr='price')
    img_url = indexes.CharField(model_attr='img_url')
    title = indexes.CharField(model_attr='title')

    def get_model(self):
        return Computer