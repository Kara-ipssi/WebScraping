import scrapy
from scrapy import Request
from MangaCrawler.items import MangaTypes, MangacrawlerItem, DataBase
import sqlalchemy as db

class MangascantradSpider(scrapy.Spider):
    name = 'mangascantrad'
    allowed_domains = ['www.japscan.me']

    # Liste des urls par pages
    start_urls_list = [f'https://www.japscan.me/mangas/{n}' for n in range(1, 31)]
    start_urls = [f'https://www.japscan.me/manga/{n}' for n in start_urls_list]

    mangas_url_list = []

    # Création de la base de données
    database = DataBase('database_manga')

    # Creation des tables avec une relation ManyToMany
    database.create_table('mangas_types',
                          id_=db.Integer,
                          name=db.String,
                          )

    database.create_table('mangas',
                          id_=db.Integer,
                          title=db.String,
                          img=db.String,
                          origin=db.String,
                          description=db.String,
                          last_chapter=db.String,
                          link=db.String,
                          type=db.String,
                          genres=db.String,
                          published_date=db.String,
                          state=db.String,
                          )

    database.create_table_relationship('mangas_assoc_types', 'mangas', 'mangas_types')

    def start_requests(self):
        # Récupérer la liste des liens
        for url in self.start_urls_list:
            # appel la fonction addlinks en asynchrone avec la response
            yield Request(url=url, callback=self.addlinks)
        # Récupérer les informations par lien manga

    def addlinks(self, response):
        items = response.css("div.p-2 p.p-1.text-center a")
        for item in items:
            domaine = "https://www.japscan.me"
            yield self.mangas_url_list.append(domaine + item.css["a"].attrib['href'])

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

