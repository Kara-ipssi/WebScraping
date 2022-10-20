import scrapy
from scrapy import Request
from MangaCrawler.items import MangaGenres, MangacrawlerItem, DataBase
import sqlalchemy as db
from sqlalchemy.orm import declarative_base, relationship

class MangascantradSpider(scrapy.Spider):
    name = 'mangascantrad'
    allowed_domains = ['manga-scantrad.net']

    # Liste des urls par pages
    start_urls = [f'http://manga-scantrad.net/manga/page/{n}' for n in range(1, 31)]

    # Création de la base de données
    database = DataBase('database_manga')

    # Creation des tables avec une relation ManyToMany
    Base = declarative_base()
    association_table = db.Table(
        "mangas_assoc_genres",
        Base.metadata,
        db.Column("mangas_id", db.ForeignKey("mangas.id_")),
        db.Column("mangas_genres_id", db.ForeignKey("mangas_genres.id_")),
    )
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
                          genres=db.String,
                          published_date=db.String,
                          state=db.String,
                          nb_comments=db.String,
                          children=relationship("mangas_genres", secondary=association_table)
                          )

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

