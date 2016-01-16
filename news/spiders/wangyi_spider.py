#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging

import scrapy
from scrapy.http.request import Request
from news.items import NewsItem

class WangyiSpider(scrapy.Spider):
    name = "wangyi"
    allowed_domains = ["163.com"]
    start_urls = ["http://news.163.com"]

    def make_requests_from_url(self, url):
        #模拟浏览器请求
        headers = {
                'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
                }
        request = Request(url, headers=headers)
        return request

    def closed(self, reason):
        pass

    def parse(self, response):
        if response.status != 200:
            self.log("get page fail:" + response.url, log.ERROR)
            return 

        f = open('a.html', 'wb')
        f.write(response.body)
        return 

        #links = response.xpath('///div[@class="ns-bg-wrap"]/div[@class="ns-area cf"]/div[@class="ns-main"]/div[@class="ns-mr60"]/div[@class="ns-wnews mb20"]/h3')
        #for index, link in enumerate(links):
        #    head_lines = link.xpath('a')
        #    for head_line in head_lines:
        #        #head_line.xpath('text()').extract_first()  #主页标题
        #        yield Request(head_line.xpath('@href').extract_first(), self.parse_head_line_page)
    
    def parse_head_line_page(self, response):
        if response.status != 200:
            self.log("get head line fail:" + response.url, log.ERROR)
            return 

        title = response.xpath('////h1/text()').extract_first()
        content = response.xpath('////div[@id="endText"]').extract_first()
        data = NewsItem()
        data['title'] = title
        data['url'] = response.url
        data['content'] = content
        return data
