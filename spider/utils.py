# -*- coding: utf-8 -*-
# @Time    : 2021/7/23 11:37
# @Author  : ShaoJK
# @File    : utils.py
# @Remark  :
from scrapy import Request
from scrapy.utils.url import escape_ajax
from w3lib.url import safe_url_string


class Dict(dict):
    """用属性的形式使用字典"""

    def __getattr__(self, key):
        if key not in self.keys():
            return None
        return self.get(key)

    def __setattr__(self, key, value):
        self[key] = value
