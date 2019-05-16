#!/usr/bin/env python
# encoding: utf-8
'''
@author: taiyc
@file: searchresult2json
@time: 2019/3/28 21:17
'''
# from haystack.models import SearchResult

def sea_result2json(list_obj):
    json = [sr.get_additional_fields() for sr in list_obj]
    return json