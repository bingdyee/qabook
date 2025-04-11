# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImageItem(scrapy.Item):
    images = scrapy.Field()
    image_urls = scrapy.Field()


class SuperItem(scrapy.Item):

    def __setitem__(self, key, value):
        if key in self.fields:
            self._values[key] = value
        else:
            self.fields[key] = scrapy.Field()
            self._values[key] = value


class BookItem(scrapy.Item):
    id = scrapy.Field()
    # 书名
    title = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 出版商
    publisher = scrapy.Field()
    # 发布时间
    publish_date = scrapy.Field()
    # 分类
    category = scrapy.Field()
    sub_category = scrapy.Field()
    # 标签
    tags = scrapy.Field()
    # 图片
    cover_url = scrapy.Field()
    # 简介
    summary = scrapy.Field()
    # 字数
    word_count = scrapy.Field()
    # 频道
    channel = scrapy.Field()
    # 来源
    source_link = scrapy.Field()
    # 状态
    status = scrapy.Field()
    # 最新章节
    last_chapter = scrapy.Field()
    chapter_update_time = scrapy.Field()
    # 章节
    chapter_list = scrapy.Field()


class AuthorItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    avatar = scrapy.Field()
    biography = scrapy.Field()
    locale = scrapy.Field()


class ChapterItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    book_id = scrapy.Field()
    part_name = scrapy.Field()
    source_link = scrapy.Field()
    update_time = scrapy.Field()
    word_count = scrapy.Field()


class NovelItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    summary = scrapy.Field()
    cover_url = scrapy.Field()
    channel = scrapy.Field()
    category_name = scrapy.Field()
    sub_category_name = scrapy.Field()
    word_count = scrapy.Field()
    read_count = scrapy.Field()
    last_chapter_title = scrapy.Field()
    last_chapter_update_time = scrapy.Field()
    status = scrapy.Field()
    chapter_list = scrapy.Field()
    tags = scrapy.Field()
    source_link = scrapy.Field()

