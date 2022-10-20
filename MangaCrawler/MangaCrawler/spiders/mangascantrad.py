import scrapy
from scrapy import Request
from MangaCrawler.items import MangaTypes, MangacrawlerItem, DataBase
import sqlalchemy as db

class MangascantradSpider(scrapy.Spider):
    name = 'mangascantrad'
    allowed_domains = ['www.japscan.me']

    # Liste des urls par pages
    start_urls_list = [f'https://www.japscan.me/mangas/{n}' for n in range(1, 31)]

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

        # Lien manga 
        try:
            item['link'] = manga.url
        except:
            item['link'] = "None"

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
            item['origin'] = manga.css('div#main div.card-body p.mb-2')[2].css('span::text')[1].get()

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
            item['type'] = 'None'
            for i in range (1, 8):
                if manga.css('div#main div.card-body p.mb-2')[i].get().split(':')[0].split('>')[2] == 'Type(s)':
                    item['type'] = manga.css('div#main div.card-body p.mb-2')[i].get().split('</span')[1].split('\t')[7].strip()
        except:
            item['type'] = 'None'

        # genres manga
        try:
            item['genres'] = 'None'
            for i in range(1, 8):
                if manga.css('div#main div.card-body p.mb-2')[i].get().split(':')[0].split('>')[2] == 'Genre(s)':
                    item['genres'] = manga.css('div#main div.card-body p.mb-2')[i].get().split('</span')[1].split('\t')[7].strip()
        except:
            item['genres'] = 'None'

        # Date du manga
        try:
            item['published_date'] = 'None'
            for i in range(1, 8):
                if manga.css('div#main div.card-body p.mb-2')[i].get().split(':')[0].split('>')[2] == 'Date Sortie':
                    item['published_date'] = manga.css('div#main div.card-body p.mb-2')[i].get().split('</span')[1].split('\t')[7].strip()
        except:
            item['published_date'] = 'None'

        # Etat manga
        try:
            stateM = manga.css('div#main div.card-body p.mb-2')[2].get().split('</span')[1].split('\t')[6].strip()
            item['state'] = stateM if stateM != '' else manga.css('div#main div.card-body p.mb-2')[3].get().split('</span')[1].split('\t')[6].strip()
        except:
            item['state'] = "None"

        # Ajouter dans la base de données
        self.database.add_row('mangas',
                              title=item['title'],
                              img=item['img'],
                              origin=item['origin'],
                              description=item['description'],
                              last_chapter=item['last_chapter'],
                              link=item['link'],
                              type=item['type'],
                              genres=item['genres'],
                              published_date=item['published_date'],
                              state=item['state']
                              )
        yield item
