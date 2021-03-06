# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 11:28
# @Author  : ShaoJK
# @File    : BiliBiliSpider.py
# @Remark  :
import time

from scrapy import Request
from spider.spiders.ChromeSpider import ChromeSpider

class BiliBiliSpider(ChromeSpider):
    name = "bilibili"
    custom_settings = { # 指定使用的piplines, piplines需要在setting里先注册
        'ITEM_PIPELINES': {'spider.pipelines.BilibiliPipeline': 300,}
    }
    output_path = "bilibili_result.json"
    def __init__(self, *args, **kwargs):
        super(BiliBiliSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        urls = [
            # ('https://www.bilibili.com/', self.parse_video_card)
            ('https://space.bilibili.com/17958944/video?tid=0&page=5&keyword=&order=pubdate')
            # ('https://space.bilibili.com/32361636/fans/follow', self.parse_subtitle)
        ]
        urls = ['https://space.bilibili.com/17958944/video?tid=0&page=%s&keyword=&order=pubdate'%i for i in range(1,3)]
        for url in urls:
            yield Request(url=url, callback=self.parse_up_list)

    def parse_subtitle(self, response):
        ele = True
        while ele:
            for item in response.xpath("//li[@class='list-item clearfix']"):
                yield {
                    "avatar": item.xpath("./a").attrib["href"].strip(),
                    "name": item.xpath(".//span[@class='fans-name']/text()").get().strip(),
                    "description": item.xpath(".//p[contains(@class,'desc')]").get().strip()
                }
            ele = self.browser.wait_appearance("//li[@class='be-pager-next']",timeout=1)
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
    
    def parse_up_list(self, response):
        for ele in response.xpath("//li[@class='small-item fakeDanmu-item']"):
            yield {
                "url": ele.xpath("./a").attrib["href"].strip(),
                "name": ele.xpath(".//a[text()]/text()").get().strip(),
                "time": ele.xpath(".//span[@class='time']/text()").get().strip()
            }