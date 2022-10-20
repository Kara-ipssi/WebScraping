import scrapy
import sqlalchemy as db


class MangacrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    img = scrapy.Field()
    rating = scrapy.Field()
    last_chapter = scrapy.Field()
    link = scrapy.Field()
    genres = scrapy.Field()
    published_date = scrapy.Field()
    state = scrapy.Field()
    nb_comments = scrapy.Field()
    pass


class MangaGenres:
    def __init__(self):
        self.list = [
            'arts-martiaux',
            'action',
            'shonen',
            'seinen',
            'shojo',
            'josei',
            'fantaisie',
            'isekai',
            'fantastique',
            'romance',
            'psychologique',
            'drame',
            'webtoons'
        ]



class DataBase():
    def __init__(self, name_database='database'):
        self.name = name_database
        self.url = f"sqlite:///{name_database}.db"
        self.engine = db.create_engine(self.url)
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()
        self.table = self.engine.table_names()

    def create_table(self, name_table, **kwargs):
        colums = [db.Column(k, v, primary_key=True) if 'id_' in k else db.Column(k, v) for k, v in kwargs.items()]
        db.Table(name_table, self.metadata, *colums)
        self.metadata.create_all(self.engine)
        print(f"*********Table : '{name_table}' are created succesfully************")

    def create_table_relationship(self, assoc_name, table_name1, table_name2):
        db.Table(
            assoc_name,
            self.metadata,
            db.Column("id_", db.Integer, primary_key=True),
            db.Column(f"{table_name1}_id", db.Integer, db.ForeignKey(f"{table_name1}.id_")),
            db.Column(f"{table_name2}_id", db.Integer, db.ForeignKey(f"{table_name2}.id_")),
        )
        self.metadata.create_all(self.engine)
        print(f"*********Table Relationship : '{assoc_name}' are created succesfully************")

    def read_table(self, name_table, return_keys=False):
        table = db.Table(name_table, self.metadata, autoload=True, autoload_with=self.engine)
        if return_keys:
            table.columns.keys()
        else:
            return table

    def add_row(self, name_table, **kwarrgs):
        name_table = self.read_table(name_table)

        stmt = (
            db.insert(name_table).
                values(kwarrgs)
        )
        self.connection.execute(stmt)
        print(f'Row id added')

    def delete_row_by_id(self, table, id_):
        name_table = self.read_table(name_table)

        stmt = (
            db.delete(name_table).
                where(students.c.id_ == id_)
        )
        self.connection.execute(stmt)
        print(f'Row id {id_} deleted')

    def select_table(self, name_table):
        name_table = self.read_table(name_table)
        stm = db.select([name_table])
        return self.connection.execute(stm).fetchall()
