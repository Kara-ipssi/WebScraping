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

        for url in self.mangas_url_list:
            yield Request(url=url, callback=self.parse_manga)

    def addlinks(self, response):
        items = response.css("div.p-2 p.p-1.text-center")
        for item in items:
            domaine = "https://www.japscan.me"
            yield self.mangas_url_list.append(domaine + item.css("a").attrib['href'])

    def parse_manga(self, response):
    # Récupérer les informations par lien manga
        manga = response
        item = MangacrawlerItem()

        # Titre manga
        try:
            item['title'] = manga.css('div#main div.card-body h1::text').get()
        except:
            item['title'] = 'None'

        # Image manga
        try:
            item['img'] = manga.css('div#main div.card-body img').attrib['src']
        except:
            item['img'] = 'None'

        # Origin manga
        try:
            item['origin'] = manga.css('div#main div.card-body p.mb-2')[1].css('span::text')[1].get()
        except:
            item['origin'] = 'None'

        # description manga
        try:
            item['description'] = manga.css('div#main div.card-body p.list-group-item.list-group-item-primary.text-justify::text').get()
        except:
            item['description'] = 'None'

        # Dernier chapitre manga
        try:
            item['last_chapter'] = manga.css('div#chapters_list div.collapse.show div.chapters_list.text-truncate').get().split(':')[0].split('\t')[-1]
        except:
            item['last_chapter'] = 'None'

        # Lien manga
        try:
            item['last_chapter'] = manga.request.url
        except:
            item['last_chapter'] = 'None'

        # Type du manga
        try:
            item['type'] = manga.css('div#main div.card-body p.mb-2')[4].get().split('</span')[1].split('\t')[7].strip()
        except:
            item['type'] = 'None'

        # genres manga
        try:
            item['genres'] = manga.css('div#main div.card-body p.mb-2')[5].get().split('</span')[1].split('\t')[7].strip()
        except:
            item['genres'] = 'None'

        # Date du manga
        try:
            item['published_date'] = manga.css('div#main div.card-body p.mb-2')[3].get().split('</span')[1].split('\t')[7].strip()
        except:
            item['published_date'] = 'None'

        # Etat manga
        try:
            item['state'] = manga.css('div#main div.card-body p.mb-2')[2].get().split('</span')[1].split('\t')[6].strip()
        except:
            item['state'] = 'None'

        # Ajouter dans la base de données
        # self.database.add_row('manga',
        #                       name=item['name'],
        #                       img=item['img'],
        #                       description=item['description']
        #                       )
        yield item 

