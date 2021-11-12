# -*- coding: utf-8 -*-
# @Time    : 2021/7/23 11:37
# @Author  : ShaoJK
# @File    : utils.py
# @Remark  :
import time


class Dict(dict):
    """用属性的形式使用字典"""

    def __getattr__(self, key):
        if key not in self.keys():
            return None
        return self.get(key)

    def __setattr__(self, key, value):
        self[key] = value

def timestamp_to_str(timestamp, format="%Y-%m-%d %H:%M:%S") -> str:
    return time.strftime(format, time.localtime(timestamp))

def str_to_timestamp(datetime, format="%Y-%m-%d %H:%M:%S") -> int:
    return time.strptime(datetime, format)
