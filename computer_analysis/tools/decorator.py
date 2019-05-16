#!/usr/bin/env python
# encoding: utf-8
'''
@author: taiyc
@file: decorator
@time: 2019/3/14 16:00
'''

from django.http import JsonResponse

def allow_origin(func):
    def _func(*args, **kwargs):
        data = func(*args, **kwargs)
        response = JsonResponse(data)
        response['Access-Control-Allow-Origin'] = '*'
        return response
    return _func