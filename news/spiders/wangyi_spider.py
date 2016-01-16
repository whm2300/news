#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import re

import scrapy
from scrapy.http.request import Request
from news.items import NewsItem

class WangyiSpider(scrapy.Spider):
    name = "wangyi"
    allowed_domains = ["163.com"]
    start_urls = ["http://news.163.com"]
    crawl_url = set()  #已经爬取的url
    url_patter = re.compile(r'/\d+/\d+/\d+/*')

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
            self.log("get page fail:" + response.url, logging.ERROR)
            return 

        linka_s = 0
        linka_e = 0
        while linka_s != -1:
            linka_s = response.body.find('<a', linka_e)
            linka_e = response.body.find('</a>', linka_s)
            url_a = response.body[linka_s:linka_e+4]
            url_s = url_a.find('http://')
            url_e = url_a.find('"', url_s)
            match = self.url_patter.search(url_a[url_s:url_e])
            if match:
                self.crawl_url.add(url_a[url_s:url_e])
                yield Request(url_a[url_s:url_e], self.parse_news_page)
    
    def parse_news_page(self, response):
        """解析新闻正文"""
        if response.status != 200:
            self.log("get head line fail:" + response.url, logging.ERROR)
            return 

        #过滤掉不合适网页
        if response.url.find('http://view') != -1:
            return 
        if response.url.find('http://caozhi') != -1:
            return 
        if response.url.find('http://renjia') != -1:
            return 

        s_str = '<h1 id="h1title" class="ep-h1">'
        e_str = '</h1>'
        s = response.body.find(s_str)
        e = response.body.find(e_str, s)

        data = NewsItem()
        data['title'] = response.body[s+len(s_str):e].decode('gb2312').encode('utf-8')
        data['url'] = response.url
        data['content'] = 'aaaaa'
        return data
