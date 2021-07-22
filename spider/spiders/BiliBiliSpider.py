# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 11:28
# @Author  : ShaoJK
# @File    : BiliBiliSpider.py
# @Remark  :
from scrapy import Spider, Request
from selenium import webdriver


class BiliBiliSpider(Spider):
    name = "Bilibili"
    def __init__(self, *args, **kwargs):
        chorme_options = webdriver.ChromeOptions()
        chorme_options.add_argument("--headless")
        chorme_options.add_argument("--disable-gpu")
        chorme_options.add_argument(r"user-data-dir=C:\Users\Almond\AppData\Local\Google\Chrome\User Data")
        self.browser = webdriver.Chrome(chrome_options=chorme_options)
        self.browser.maximize_window()
        super(BiliBiliSpider, self).__init__(*args, **kwargs)

    @staticmethod
    def close(spider, reason):
        print(type(reason), reason)
        spider.browser.quit()

    def start_requests(self):
        urls = [
            'https://www.bilibili.com/'
        ]
        for url in urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        for ele in response.xpath("//div[@class='video-card-common']"):
            yield {
                "href": ele.xpath("./a").attrib["href"],
                "title": ele.xpath("./a[@title]/@title").get(),
                "up": ele.xpath("./a[@class='up']/text()").get()
            }
        # page = response.url.split("/")[-2]
        # filename = f'quotes-{page}.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log(f'Saved file {filename}')