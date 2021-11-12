# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 11:28
# @Author  : ShaoJK
# @File    : Tmall.py
# @Remark  :
import time
import json

from scrapy import Request

from spider.spiders.ChromeSpider import ChromeSpider


class TmallSpider(ChromeSpider):
    # custom_setting = { # 指定使用的piplines, piplines需要在setting里先注册
    #     'ITEM_PIPLINES': {}
    # }
    def __init__(self, *args, **kwargs):
        super(TmallSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        self.login()
        self.to_sycm()
        self.synchronize_cookies()
        dateRange = "2021-10-31%7C2021-10-31"
        items = ["600432180151"]
        for itemId in items:
            yield self.get(f'https://sycm.taobao.com/flow/v6/live/item/source.json?dateRange={dateRange}&dateType=today"\
                "&order=desc&orderBy=uv&device=2&itemId={itemId}&indexCode=uv&_={self.timestamp}&token=59c179268', 
                callback=self.parse_item)

    def parse_item(self, response):
        source = json.loads(response.text().encode('utf-8').decode('unicode_escape'))
        for item in source['data']['data']:
            data = dict()
            for key,value in item.items():
                if type(value) == list:
                    child = dict()
                    for child_item in value:
                        for child_key,child_value in child_item.items():
                            child[child_key] = child_value['value']
                        yield child
                elif 'value' in value.keys():
                    data[key] = value['value']
            yield data

    def login(self):
        self.driver.get("https://www.tmall.com")
        ele = self.driver.wait_appearance("//*[contains(@class,'j_Username') and text()='%s']"%self.config.TMALL_ACCOUNT, timeout=5)
        if ele is None:
            self.driver.get("https://login.tmall.com/")
            url = self.driver.get_visibility_element('//iframe').get_attribute("src")
            self.driver.get(url)
            ele = self.driver.get_visibility_element("//input[@name='fm-login-id']", timeout=3)
            self.driver.input(ele,self.config.TMALL_ACCOUNT)
            ele = self.driver.get_visibility_element("//input[@name='fm-login-password']")
            self.driver.input(ele,self.config.TMALL_PASSWORD)
            self.driver.click_by_content("登录")
            self.driver.get_visibility_element("//*[contains(@class,'j_Username') and text()='%s']"%self.config.TMALL_ACCOUNT)

    def to_sycm(self):
        """跳转到生意参谋"""
        self.driver.get("https://sycm.taobao.com")
        time.sleep(3)

    def to_myseller(self):
        """跳转到天猫商家"""
        self.driver.get("https://myseller.taobao.com")
