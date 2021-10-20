# -*- coding: utf-8 -*-
# @Time    : 2021/7/23 11:13
# @Author  : ShaoJK
# @File    : ChromeSpider.py
# @Remark  : 使用Selenium Chrome进行数据爬取通用类
import time

from scrapy import Spider
from scrapy.http import HtmlResponse
from selenium import webdriver

from spider.browser import BrowserDriver
from spider.utils import Dict


class ChromeSpider(Spider):
    def __init__(self, config=None, *args, **kwargs):
        super(ChromeSpider, self).__init__(*args, **kwargs)
        self.config = config
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        if self.config.HEADLESS:
            options.add_argument("--headless")
            options.add_argument("--window-size=1960,1080")
            options.add_argument("--disable-gpu")
        if self.config.USER_DATA:
            options.add_argument(r"user-data-dir=%s" % self.config.USER_DATA)
        self.browser = BrowserDriver(chrome_options=options)
        # self.browser = webdriver.Chrome(chrome_options=options)
        self.browser.set_page_load_timeout(0.5)
        try:
            time.sleep(0.5)
            self.browser.get("chrome://version/")
        except Exception as e:
            print(e)
        self.browser.set_page_load_timeout(60)

    @staticmethod
    def close(spider, reason):
        spider.browser.quit()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        config = Dict({
            "USER_DATA": crawler.settings.get("USER_DATA"),
            "HEADLESS": crawler.settings.get("HEADLESS")
        })
        return super().from_crawler(crawler, config=config,  *args, **kwargs)

    def getResponse(self):
        """获取当前页面的Response对象"""
        self.browser.loadPage()
        return HtmlResponse(url=self.browser.current_url, body=self.browser.page_source, encoding="utf8")
