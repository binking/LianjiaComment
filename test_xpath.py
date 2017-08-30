#!/usr/bin/python3
import re
import requests
from scrapy import Selector

house_item = {}

r = requests.get("https://bj.lianjia.com/zufang/101101886923.html")
selector = Selector(text=r.text)
content_selector = selector.xpath('//div[@class="content-wrapper"]') or selector.xpath('/html/body/div[4]')
# house_item['house_id'] = 
# house_item['view_count'] = 
# house_item['community_id']
title_selector = content_selector.xpath('.//div[@class="title"]')
if title_selector:
    house_item['house_name'] = title_selector[0].xpath('.//*[@class="main"]/text()').extract()[0].strip() 
    house_item['house_desc'] = title_selector[0].xpath('.//*[@class="sub"]/text()').extract()[0].strip()
house_item['price'] = content_selector.xpath('.//div[@class="price "]/*[@class="total"]/text()').re(r'\d+')[0]
detail_selector = content_selector.xpath('.//div[@class="zf-room"]')
room_info_str = ''.join(detail_selector.xpath(".//text()").extract()).strip()
# house_item['house_tags']
if len(room_info_str) > 1:
    house_item['square_footage'] = re.search(r'面积：(.+?)房屋', room_info_str).group(1)
    house_item['house_type'] = re.search(r'房屋户型：(.+)\n', room_info_str).group(1)
    house_item['house_floor'] = re.search(r'楼层：(.+?)房屋', room_info_str).group(1)
    house_item['orientation'] = re.search(r'朝向：(.+?)\n', room_info_str).group(1)
    house_item['subway'] = re.search(r'地铁：(.+?)\n', room_info_str).group(1)
    house_item['community_name'] = re.search(r'小区：(.+?)\n', room_info_str).group(1)
    house_item['location'] = re.search(r'位置：(.+?)\n', room_info_str).group(1)
    house_item['publish_time'] = re.search(r'时间：(\S+)', room_info_str).group(1)
# house_item['update_time']
resource_intro = selector.xpath('.//div[@id="introduction"]')
resource_intro_str = ''.join(resource_intro.xpath(".//text()").extract()).strip()
if resource_intro:
    house_item['rental_method'] = re.search(r'租赁方式：(\S+)\s+', resource_intro_str).group(1)
    house_item['pay_method'] = re.search(r'付款方式：\s*(\S+)\s+', resource_intro_str).group(1)
    house_item['vacancy_status'] = re.search(r'房屋现状：(\S+)\s+', resource_intro_str).group(1)
    house_item['heating_method'] = re.search(r'供暖方式：(\S+)\s+',
                                             resource_intro_str).group(1)
house_item['facility'] = '|'.join(resource_intro.xpath('.//li[contains(@class, "tags")]/text()').re('\S+'))
feature_content = resource_intro.xpath('.//div[@class="featureContent"]')[0]
feature_dict = dict()
# import pdb; pdb.set_trace()
for label, text in zip(feature_content.xpath('.//*[@class="label"]/text()'), feature_content.xpath('.//*[@class="text"]/text()')):
    feature_dict[label.extract()[:-1]] = text.extract()
house_item['house_feature'] = feature_dict
image_selector = content_selector.xpath('.//div[@id="topImg"]')[0]
images_dict = dict()
for li_tag in image_selector.xpath('.//li'):
    image_url = li_tag.xpath('@data-src').extract()[0]
    image_name = li_tag.xpath('@data-desc').extract()[0]
    images_dict[image_name] = image_url
house_item['images'] = images_dict
# house_item['crawl_time'] = get_now()
# house_item['image_paths']
for k, v in house_item.items():
    print(k,)
    print(v)

