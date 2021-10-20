# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 11:28
# @Author  : ShaoJK
# @File    : BiliBiliSpider.py
# @Remark  :
import time

from scrapy import Request
from spider.spiders.ChromeSpider import ChromeSpider

class BiliBiliSpider(ChromeSpider):
    name = "Bilibili"
    def __init__(self, *args, **kwargs):
        super(BiliBiliSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        urls = [
            ('https://www.bilibili.com/', self.parse_video_card)
            # ('https://space.bilibili.com/32361636/fans/follow', self.parse_subtitle)
        ]
        for url,callback in urls:
            yield Request(url=url, callback=callback)

    def parse_subtitle(self, response):
        ele = True
        while ele:
            for item in response.xpath("//li[@class='list-item clearfix']"):
                yield {
                    "avatar": item.xpath("./a").attrib["href"].strip(),
                    "name": item.xpath(".//span[@class='fans-name']/text()").get().strip(),
                    "description": item.xpath(".//p[contains(@class,'desc')]").get().strip()
                }
            ele = self.browser.wait_appearance("//li[@class='be-pager-next']",timeout=3)
            if ele:
                self.browser.click_direct(ele)
                time.sleep(0.5)
                response = self.getResponse()

    def parse_video_card(self, response):
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