from logging import warn
from optparse import OptionParser

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def run_spiders(spiders, output=None):
    setting = get_project_settings()
    setting.update({"FEED_URI":"test.json"})
    process = CrawlerProcess(setting)
    register_spiders = process.spider_loader.list()
    for spider in spiders:
        if spider in register_spiders:
            print("Running spider %s" % (spider))
            process.crawl(spider)
        else:
            warn("Spider<%s>不存在"%spider)
    process.start()

if __name__ == "__main__":
    parse = OptionParser()
    parse.add_option("-s", "--spiders", dest="spiders", default=[], action="store", help="assign spiders")
    parse.add_option("-o", "--output", dest="FEED_URI", default=None, action="store", help="set result output path")
    parse.add_option("--debug", "--debug", dest="debug", default=False, action="store_true",
                     help="specify a tenant id")
    parse.add_option("--headless", "--headless", dest="headless", default=False, action="store_true",
                     help="launch selenium headless")
    option, args = parse.parse_args()
    run_spiders(option.spiders.split(","))
