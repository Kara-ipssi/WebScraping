import scrapy
from scrapy import Request
from MangaCrawler.items import MangaGenres, MangacrawlerItem, DataBase
import sqlalchemy as db
from sqlalchemy.orm import declarative_base, relationship

class MangascantradSpider(scrapy.Spider):
    name = 'mangascantrad'
    allowed_domains = ['www.japscan.me']

    # Liste des urls par pages
    start_urls_list = [f'http://www.japscan.me/mangas/{n}' for n in range(1, 31)]
    start_urls = [f'http://www.japscan.me/mangas/{n}' for n in start_urls_list]

    # Création de la base de données
    database = DataBase('database_manga')

    # Creation des tables avec une relation ManyToMany
    database.create_table('mangas_genres',
                          id_=db.Integer,
                          name=db.String,
                          )

    database.create_table('mangas',
                          id_=db.Integer,
                          title=db.String,
                          img=db.String,
                          rating=db.String,
                          last_chapter=db.String,
                          link=db.String,
                          published_date=db.String,
                          state=db.String,
                          nb_comments=db.String,
                          )

    database.create_table_relationship('mangas_assoc_genres', 'mangas', 'mangas_genres')

    def start_requests(self):
        print("iok")
        # for url in self.start_urls:
        #     yield Request(url=url, callback=self.parse_manga)

    def parse_manga(self, response):
        mangas = response.css('div.js-categories-seasonal.js-block-list.list table tr')[1:]
        for manga in mangas:
            item = MangacrawlerItem()

            # Nom manga
            try:
                item['name'] = manga.css('td')[1].css('a.hoverinfo_trigger.fw-b strong::text').get()
            except:
                item['name'] = 'None'

            # Image manga
            try:
                item['img'] = manga.css('td')[0].css('a.hoverinfo_trigger img').attrib['data-src']
            except:
                item['img'] = 'None'

            # Description manga
            try:
                item['description'] = manga.css('td')[1].css('div.pt4::text').get()
            except:
                item['description'] = 'None'

            # Ajouter dans la base de données
            self.database.add_row('manga',
                                  name=item['name'],
                                  img=item['img'],
                                  description=item['description']
                                  )
            yield item

