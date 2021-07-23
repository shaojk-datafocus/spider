# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 11:28
# @Author  : ShaoJK
# @File    : BiliBiliSpider.py
# @Remark  :
import time

from scrapy import Request
from scrapy.http import HtmlResponse

from spider.spiders.ChromeSpider import ChromeSpider


class BiliBiliSpider(ChromeSpider):
    name = "Bilibili2"
    def __init__(self, *args, **kwargs):
        super(BiliBiliSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        urls = [
            # ('https://www.bilibili.com/', self.parse_video_card)
            ('https://space.bilibili.com/32361636/fans/follow', self.parse_subtitle)
        ]
        for url,callback in urls:
            yield Request(url=url, callback=callback)

    def parse_subtitle(self, response):
        for i in range(3):
            self.browser.click_direct(self.browser.get_visibility_element("//li[@class='be-pager-next']",timeout=3))
            time.sleep(0.5)
            self.browser.loadPage()
            print("点击了翻页")
            yield Request(url=response.url, callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):
        for ele in response.xpath("//li[@class='list-item clearfix']"):
            # print("爬取了内容")
            yield {
                "avatar": ele.xpath("./a").attrib["href"].strip(),
                "name": ele.xpath(".//span[@class='fans-name']/text()").get().strip(),
                "description": ele.xpath(".//p[contains(@class,'desc')]").get().strip()
            }

    def parse_vide_card(self, response):
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