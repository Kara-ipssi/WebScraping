import scrapy
from MangaCrawler.items import MangaGenres, DataBase

class MangascantradSpider(scrapy.Spider):
    name = 'mangascantrad'
    allowed_domains = ['manga-scantrad.net']

    # Liste des urls par pages
    start_urls1 = ['http://manga-scantrad.net/manga/']
    start_urls2 = [f'http://manga-scantrad.net/manga/page/{n}' for n in range(1, 31)]
    start_urls = start_urls1 + start_urls2

    def parse(self, response):
        pass
