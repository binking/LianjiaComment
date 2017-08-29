from scrapy.crawler import CrawlerProcess
from LianjiaCommunity.spiders.CommunitySpider import CommunityCommentSpider

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(CommunityCommentSpider)
    process.start()

