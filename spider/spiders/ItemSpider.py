# -*- coding: utf-8 -*-
# @Time    : 2021/11/12 14:44
# @Author  : ShaoJK
# @File    : ItemSpider.py
# @Remark  : 爬取商品信息
import json

from spider.spiders.TmallSpider import TmallSpider


class ItemSpider(TmallSpider):
    name = "item"
    custom_setting = { # 指定使用的piplines, piplines需要在setting里先注册
        'ITEM_PIPLINES': {'spider.pipelines.ItemPipeline': 300}
    }
    def __init__(self, items, date, *args, **kwargs):
        super(TmallSpider, self).__init__(*args, **kwargs)
        self.items = items.split(",")
        self.date = date
        self.login()
        self.to_sycm()
        self.synchronize_cookies()

    def start_requests(self):
        # 获取商品的基础信息
        for itemId in self.items:
            yield self.get(f"https://sycm.taobao.com/cc/item/crowd/info.json?itemId={itemId}&"
                           f"dateType=day&dateRange={self.date}%7C{self.date}&_={self.timestamp}", callback=self.parse)

    def parse(self, response):
        source = json.loads(response.text().encode('utf-8').decode('unicode_escape'))
        yield source['data']