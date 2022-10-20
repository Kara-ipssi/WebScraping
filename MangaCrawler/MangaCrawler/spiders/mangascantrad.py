import scrapy


class MangascantradSpider(scrapy.Spider):
    name = 'mangascantrad'
    allowed_domains = ['manga-scantrad.net']
    start_urls = ['http://manga-scantrad.net/']

    def parse(self, response):
        pass
