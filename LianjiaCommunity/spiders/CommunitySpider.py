# -*- coding: utf-8 -*-
import re
import json
import scrapy
import traceback
# from scrapy_redis.spiders import RedisSpider
from LianjiaCommunity.items import LianjiacommunityCommentItem
from scrapy.selector import Selector
from scrapy.http import Request

def get_now():
    return "2017-08-29"


class CommunityCommentSpider(scrapy.Spider):
# class CommunityspiderSpider(RedisSpider):
    name = 'CommunityCommentSpider'
    redis_key = 'LianjiaCommunityCommentSpider:start_urls'
    # allowed_domains = ['https://m.lianjia.com/']
    start_urls = ['https://m.lianjia.com/bj/xiaoqu/1111027382209/dianping/?page=1&page_size=20&_t=1/']
    COMMENT_FILE = "./LianjiaCommunity/files/lianjia_community_comment_{cid}_{date}_page_{page}.html"
    # COMMENT_JSON = "./LianjiaCommunity/files/lianjia_community_comment_{cid}_{date}_{page}.json"
    COMMENT_URL = "https://m.lianjia.com/bj/xiaoqu/{cid}/dianping/?page={page}&page_size=20&_t=1"
    # OTHER_COMMENT_URL = "https://m.lianjia.com/bj/xiaoqu/{cid}/dianping/?page={page}&page_size=20&_t=1"

    def parse_json(self, response):
        """
        
        :param response: 
        :return: 
        """
        # import ipdb; ipdb.set_trace()
        current_url = response.request.url
        community_id = re.search(r'/xiaoqu/(\d+)/dianping', current_url).group(1)
        current_page = int(re.search(r'page=(\d+)', current_url).group(1))
        print >>open(self.COMMENT_JSON.format(cid=community_id, date=get_now(), page=current_page), 'w'), response.body
        try:
            comment_data = json.loads(response.body)
        except ValueError as e:
            traceback.print_exc()
            return
        if comment_data['errno'] != 0:
            print("Error Message From Lianjia: ", comment_data['errmsg'])
        comment_data = comment_data['data']
        for comment in comment_data['list']:
            comment_item = LianjiacommunityCommentItem()
            comment_item['community_id'] = str(comment_data['resblock_id'])
            comment_item['comment_id'] = comment['id']
            comment_item['user_name'] = comment['creator_name']
            comment_item['publish_date'] = comment['ctime']
            comment_item['content'] = comment['content']
            comment_item['praise_count'] = comment['praise_count']
            yield comment_item
        if comment_data['has_more_data'] == True:
            next_url = self.COMMENT_URL.format(cid=community_id) + self.OTHER_COMMENT_URL.format(cid=community_id, page=current_page+1)
            next_request = Request(next_url, callback="parse_json")
            next_request.headers['Accept'] = "application/json"
            yield next_request

    def parse(self, response):
        # print(response.body, file=open(COMMENT_FILE, 'w'))
        current_url = response.request.url
        community_id = re.search(r'/xiaoqu/(\d+)/dianping', current_url).group(1)
        current_page = int(re.search(r'page=(\d+)', current_url).group(1))
        print >>open(self.COMMENT_FILE.format(cid=community_id, date=get_now(), page=current_page), 'w'), response.body
        selector = Selector(response)
        comment_list = selector.xpath('//ul[@class="comment_ul"]')
        for li_tag in comment_list.xpath(".//li[@data-info]"):
            comment_item = LianjiacommunityCommentItem()
            comment_item['community_id'] = community_id
            comment_item['comment_id'] = li_tag.xpath('@data-info').re('\d+')[0]
            user_name = li_tag.xpath('.//p[@class="user_name"]/text()').extract()
            comment_item['user_name'] = user_name[0].strip() if user_name else ''
            # comment_item['user_tag'] = user_info[0].xpath('.//*[@class="identity_tag"]/text()')[0].extract()
            comment_date = li_tag.xpath('.//*[@class="time gray"]/text()').extract()
            comment_item['publish_date'] = comment_date[0].strip() if comment_date else ''
            content = li_tag.xpath('.//div[@data-mark="comment_content"]/text()').extract()
            comment_item['content'] = content[0].strip() if content else ''
            praise = li_tag.xpath('.//*[@data-mark="praise_count"]/text()').extract()
            comment_item['praise_count'] = int(praise[0]) if praise else 0
            yield comment_item
        if "1" in comment_list.xpath("@data-info").extract()[0]:
        # import ipdb; ipdb.set_trace()
        # next_request = Request(current_url[:-1] + self.OTHER_COMMENT_URL.format(cid=community_id, page=2), callback=self.parse_json, dont_filter=True)
            next_request = Request(self.COMMENT_URL.format(cid=community_id, page=current_page + 1), callback=self.parse)
            yield next_request

"""
Comments
first page:
curl 'https://m.lianjia.com/bj/xiaoqu/1111027382209/dianping/?page=1&page_size=20&_t=1' 
-H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4' 
-H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36' 
-H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' 
-H 'Connection: keep-alive' --compressed
-H 'Cookie: lianjia_uuid=db6803dc-f665-4b8b-86ff-170103575fb0; UM_distinctid=15e26f6d65d692-04f19344b2bb03-c313760-100200-15e26f6d65e7b2; select_nation=1; lj-ss=6485872ceb47bae3bb766e49c70d5cef; gr_user_id=a6c052da-573a-489e-9cf5-94236c6bde24; select_city=110000; CNZZDATA1254525948=451824707-1503905939-%7C1503913000; CNZZDATA1253491255=614627566-1503904117-%7C1503915124; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1503892263; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1503973118; _smt_uid=59a39328.477d8d83; _gat=1; _gat_past=1; _gat_global=1; _gat_new_global=1; _ga=GA1.2.545697752.1503892268; _gid=GA1.2.1317513514.1503892268; _gat_dianpu_agent=1; lianjia_ssid=ccc3ed18-a91a-47a5-8119-2bb7162fa792' 
second page:
curl 'https://m.lianjia.com/bj/xiaoqu/1111027382209/dianping/?page=1&page_size=20&_t=1https://m.lianjia.com/bj/xiaoqu/1111027382209/dianping/?page=2&page_size=20&_t=1' 
-H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4' 
-H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36' 
-H 'Accept: application/json' -H 'Referer: https://m.lianjia.com/bj/xiaoqu/1111027382209/dianping/?page=1&page_size=20&_t=1' 
-H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --compressed    
-H 'Cookie: lianjia_uuid=db6803dc-f665-4b8b-86ff-170103575fb0; UM_distinctid=15e26f6d65d692-04f19344b2bb03-c313760-100200-15e26f6d65e7b2; select_nation=1; lj-ss=6485872ceb47bae3bb766e49c70d5cef; gr_user_id=a6c052da-573a-489e-9cf5-94236c6bde24; select_city=110000; _smt_uid=59a39328.477d8d83; _gat=1; _gat_past=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1; lianjia_dianping_annocement_cd=1; _ga=GA1.2.545697752.1503892268; _gid=GA1.2.1317513514.1503892268; _gat_new=1; CNZZDATA1254525948=451824707-1503905939-%7C1503968984; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1503892263; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1503973167; CNZZDATA1253491255=614627566-1503904117-%7C1503970353; lianjia_ssid=ccc3ed18-a91a-47a5-8119-2bb7162fa792' 

"""