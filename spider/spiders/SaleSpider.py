# -*- coding: utf-8 -*-
# @Time    : 2021/11/12 14:44
# @Author  : ShaoJK
# @File    : SaleSpider.py
# @Remark  : 爬取销售信息
import json

from spider.spiders.TmallSpider import TmallSpider


class SaleSpider(TmallSpider):
    name = "sale"
    custom_setting = {  # 指定使用的piplines, piplines需要在setting里先注册
        'ITEM_PIPLINES': {'spider.pipelines.ItemPipeline': 300}
    }
    def __init__(self, items, dateRange, *args, **kwargs):
        super(TmallSpider, self).__init__(*args, **kwargs)
        self.items = items.split(",")
        self.dateRange = dateRange # 2021-11-01%7C2021-11-07
        self.login()
        self.to_sycm()
        self.synchronize_cookies()

    def start_requests(self):
        # 获取商品的基础信息
        for itemId in self.items:
            yield self.get(f"https://sycm.taobao.com/cc/item/sale/sku/list.json?dateRange={self.dateRange}&"
                           f"dateType=recent7&pageSize=10&page=1&order=desc&orderBy=cartCnt&device=0&itemId={itemId}&"
                           f"indexCode=cartCnt%2CpayAmt%2CpayByrCnt&_={self.timestamp}", callback=self.parse,
                           cb_kwargs={'itemId':itemId,'page':1})

    def parse(self, response, itemId, page):
        source = json.loads(response.text().encode('utf-8').decode('unicode_escape'))
        data = source['data']
        for item in data['data']:
            yield item
        if data['recordCount']>10*page: # 使用递归的方式进行翻页
            yield self.get(f"https://sycm.taobao.com/cc/item/sale/sku/list.json?dateRange={self.dateRange}&"
                           f"dateType=recent7&pageSize=10&page=1&order=desc&orderBy=cartCnt&device=0&itemId={itemId}&"
                           f"indexCode=cartCnt%2CpayAmt%2CpayByrCnt&_={self.timestamp}", callback=self.parse,
                           cb_kwargs={'itemId':itemId,'page':page+1})
