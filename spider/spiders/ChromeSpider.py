# -*- coding: utf-8 -*-
# @Time    : 2021/7/23 11:13
# @Author  : ShaoJK
# @File    : ChromeSpider.py
# @Remark  : 使用Selenium Chrome进行数据爬取通用类
import time

from scrapy import Spider
from scrapy import Request
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
        options.add_experimental_option('excludeSwitches',['enable-automation'])
        options.add_argument("--disable-blink-features=AutomationControlled")
        if self.config.HEADLESS:
            options.add_argument("--headless")
            options.add_argument("--window-size=1960,1080")
            options.add_argument("--disable-gpu")
        if self.config.USER_DATA:
            options.add_argument(r"user-data-dir=%s" % self.config.USER_DATA)
        self.driver = BrowserDriver(chrome_options=options)
        self.driver.set_page_load_timeout(0.5)
        try:
            self.driver.get("chrome://version/")
        except Exception as e:
            print(e)
        self.driver.set_page_load_timeout(60)
        self.headers = {
            'accept':'*/*',
            'accept-encoding':'gzip, deflate, br',
            'accept-language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
            'sec-fetch-mode':'cors',
            'sec-fetch-site':'same-origin',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
        }
        self.cookies = dict()

    @staticmethod
    def close(spider, reason):
        spider.driver.quit()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        config = Dict(crawler.settings.get("GLOBAL_CONFIG"))
        return super().from_crawler(crawler, config=config,  *args, **kwargs)

    @property
    def timestamp(self):
        return str(int(time.time()*1000))

    def getResponse(self, loadPage=True):
        """获取当前页面的Response对象"""
        if loadPage:
            self.driver.loadPage()
        return HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding="utf8")

    def get(self, url, callback, **kwargs):
        """发送get请求"""
        return Request(url=url, callback=callback, method='GET', headers=self.headers, cookies=self.cookies, **kwargs)

    def post(self, url, callback, **kwargs):
        """发送post请求"""
        return Request(url=url, callback=callback, method='POST', headers=self.headers, cookies=self.cookies, **kwargs)

    def synchronize_cookies(self):
        self.cookies = dict()
        for cookie in self.driver.get_cookies():
            self.cookies[cookie['name']] = cookie['value']

    def parse_example(self, response):
        for ele in response.xpath("//div[@class='video-card-common']"):
            yield {
                "href": ele.xpath("./a").attrib["href"].strip(),
                "title": ele.xpath("./a[@title]/@title").get().strip(),
                "up": ele.xpath("./a[@class='up']/text()").get().strip()
            }
        # page = response.url.split("/")[-2]
        # filename = f'quotes-{page}.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log(f'Saved file {filename}')