# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import json
import redis
import pymysql
import pymongo
from crawler import settings


class Save2MongoPipeline:

    def __init__(self, host=settings.MONGO_HOST, port=settings.MONGO_PORT, db=settings.MONGO_DB, batch_size=1000):
        self.client = pymongo.MongoClient(host, port)
        self.db = self.client[db]
        self.items = []
        self.batch_size = batch_size
        self.collection = None
        self.support_spiders = ['lxds', 'zhui', 'luoxia']

    def open_spider(self, spider):
        if spider.name in self.support_spiders:
            self.collection = self.db[spider.name]

    def process_item(self, item, spider):
        if spider.name not in self.support_spiders:
            return item
        self.add_item(item)
        if len(self.items) >= self.batch_size:
            self.save_batch()
        return item

    def save_batch(self):
        if len(self.items):
            self.collection.insert_many(self.items)
            self.items.clear()

    def close_spider(self, spider):
        if spider.name in self.support_spiders:
            self.save_batch()
            self.client.close()

    def add_item(self, item):
        self.items.append(dict(item))


class Save2MySQLPipeline:

    def __init__(self):
        self.batch_size = 500
        self.items = []
        self.support_spiders = ['lxdsc']
        self.insert_sql = 'insert into sci_chapter_content(chapter_id, content) values (%s, %s)'
        self.conn = None

    def process_item(self, item, spider):
        if spider.name not in self.support_spiders:
            return item
        self.add_item(item)
        if len(self.items) >= self.batch_size:
            self.save_batch()
        return item

    def save_batch(self):
        if len(self.items):
            with self.conn.cursor() as cursor:
                cursor.executemany(self.insert_sql, self.items)
                self.items.clear()
            self.conn.commit()

    def open_spider(self, spider):
        self.conn = pymysql.connect(host=settings.MYSQL_HOST, port=settings.MYSQL_PORT, user=settings.MYSQL_USER,
                                    password=settings.MYSQL_PWD, database=settings.MYSQL_DB)

    def close_spider(self, spider):
        self.save_batch()
        self.conn.close()

    def add_item(self, item):
        self.items.append((item['chapter_id'], item['content']))


class SaveUrls2RedisPipeline:

    def __init__(self):
        self.batch_size = 1000
        self.cache_values = []
        self.client = None
        self.cache_key = None

    def process_item(self, item, spider):
        if spider.name.startswith('pre'):
            self.add_values(item)
            if len(self.cache_values) >= self.batch_size:
                self.save_batch()
        return item

    def save_batch(self):
        pipe = self.client.pipeline()
        for cache_value in self.cache_values:
            pipe.lpush(self.cache_key, json.dumps(cache_value))
        pipe.execute()
        self.cache_values.clear()

    def open_spider(self, spider: scrapy.Spider):
        self.client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        self.cache_key = '%s_spider:start_urls' % spider.name

    def close_spider(self, spider):
        if len(self.cache_values) > 0:
            self.save_batch()
        self.client.close()

    def add_values(self, item):
        for url in item['urls']:
            cache_value = {"url": url}
            if item['has_meta']:
                cache_value["meta"] = {"cate": item['cate'], 'chan': item['chan']}
            self.cache_values.append(cache_value)


class SaveNovels2MySQLPipeline:

    def __init__(self):
        self.conn = None
        self.batch_size = 500
        self.items = []
        self.support_spiders = ['qbmfxs']
        self.cate_list = []
        self.insert_sql = """
                insert into novel_book(
                    id, title, author, 
                    summary, cover_url, channel, 
                    category_id, category_name, sub_category_id, 
                    sub_category_name, word_count, read_count, 
                    last_chapter_id, last_chapter_title, last_chapter_update_time, 
                    status
                ) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

    def open_spider(self, spider):
        self.conn = pymysql.connect(host=settings.MYSQL_HOST, port=settings.MYSQL_PORT, user=settings.MYSQL_USER,
                                    password=settings.MYSQL_PWD, database="novels", cursorclass=pymysql.cursors.DictCursor)
        with self.conn.cursor() as cursor:
            cursor.execute('select id, parent_id, category_name from novel_category')
            self.cate_list = cursor.fetchall()

    def process_item(self, item, spider):
        if spider.name not in self.support_spiders:
            return item
        self.add_item(item)
        if len(self.items) >= self.batch_size:
            self.save_batch()
        return item

    def close_spider(self, spider):
        self.save_batch()
        self.conn.close()

    def save_batch(self):
        if len(self.items):
            with self.conn.cursor() as cursor:
                cursor.executemany(self.insert_sql, self.items)
                self.items.clear()
            self.conn.commit()

    def add_item(self, item):
        cate_id, sub_cate_id = 0, 0
        for cate in self.cate_list:
            if cate['category_name'] == item['sub_cate']:
                cate_id = cate['id'] if cate['parent_id'] == 0 else cate['parent_id']
                sub_cate_id = cate['id']
        self.items.append((
            item['id'], item['title'], item['author'],
            item['summary'], item['cover_url'], item['chan'],
            cate_id, item['cate'], sub_cate_id,
            item['sub_cate'], item['word_count'], item['read_count'],
            item['last_chapter_id'], item['last_chapter_title'], item['last_chapter_update_time'],
            item['status']
        ))



