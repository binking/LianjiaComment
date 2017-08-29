# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiacommunityCommentItem(scrapy.Item):
    # define the fields for your item here like:
    community_id = scrapy.Field()
    comment_id = scrapy.Field()
    user_name = scrapy.Field()
    user_tag = scrapy.Field()
    publish_date = scrapy.Field()
    content = scrapy.Field()
    praise_count = scrapy.Field()

