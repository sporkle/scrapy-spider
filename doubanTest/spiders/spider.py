#!/usr/bin/python
# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from doubanTest.items import DoubantestItem

class Douban(CrawlSpider):
    name = "douban"
    redis_key = 'douban:start_urls'
    start_urls = ['http://movie.douban.com/top250']

    url = 'http://movie.douban.com/top250'

    def parse(self,response):
        # print response.body
        item = DoubantestItem()
        selector = Selector(response)
        Movies = selector.xpath('//div[@class="info"]')
        for eachMoive in Movies:
            title = eachMoive.xpath('div[@class="hd"]/a/span/text()').extract()
            fullTitle = ''
            for each in title:
                fullTitle += each
                # print fullTitle
            movieInfo = eachMoive.xpath('div[@class="bd"]/p/text()').extract()
            star = eachMoive.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()
            quote = eachMoive.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            #quote可能为空，因此需要先进行判断
            if quote:
                quote = quote[0]
                print quote
            else:
                quote = ''
            item['title'] = fullTitle
            item['movieInfo'] = ';'.join(movieInfo)
            item['star'] = star
            item['quote'] = quote
            # print fullTitle
            yield item

        nextLink = selector.xpath('//*[@id="content"]/div/div[1]/div[2]/span[3]/a/@href').extract()
        #最后一页没有下一页 以此为循环的结束
        if nextLink:
            nextLink = nextLink[0]
            print nextLink
            yield Request(self.url + nextLink,callback=self.parse)