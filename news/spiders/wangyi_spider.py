#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import re

import scrapy
from scrapy.http.request import Request
from news.items import NewsItem

class AnalyseHtml(object):
    crawl_url = set()  #已经爬取的url
    url_patter = re.compile(r'/\d{2}/\d{4}/\d+/*')
    news_date = '150101'
    special_url = ["v.auto.163.com/"]

    def GetAllUrl(self, body):
        """获取网页中所有url"""
        linka_s = 0
        linka_e = 0
        urls = []
        while linka_s != -1:
            linka_s = body.find('<a', linka_e)
            linka_e = body.find('</a>', linka_s)
            url_a = body[linka_s:linka_e+4]
            url_s = url_a.find('http://')
            url_e = url_a.find('"', url_s)
            url = url_a[url_s:url_e]
            if not self.Is163Url(url) or url in self.crawl_url:
                continue
            self.crawl_url.add(url)
            urls.append(url)
        return urls

    def GetNewsUrl(self, body):
        """获取新闻内容url, 该类url需满足一定正则表达式格式。"""
        urls = self.GetAllUrl(body)
        for url in urls:
            if not self.Is163Url(url) or not self.IsNewsUrl(url):
                urls.remove(url)
        return urls

    def IsNewsUrl(self, url):
        """判断url是否符合新闻内容类url"""
        match = self.url_patter.search(url)
        if match:
            date = match.group().replace('/', '')
            if date >= self.news_date:
                return True 
        return False 

    def Is163Url(self, url):
        """检测是否是网易url"""
        #体育#娱乐#财经#汽车#科技#手机#数码#女人#旅游#深圳房产#家居#教育#游戏#健康#彩票#酒香
        eligible_urls = ["sports.163.com", "ent.163.com", "money.163.com", "auto.163.com", 
                "tech.163.com", "mobile.163.com", "digi.163.com", "lady.163.com", 
                "travel.163.com", "sz.house.163.com", "home.163.com", "edu.163.com", 
                "play.163.com", "jiankang.163.com", "caipiao.163.com", "jiu.163.com", 
                "news.163.com", ]
        for i in eligible_urls:
            if (url.find(i) != -1):
                return True
        return False

class WangyiSpider(scrapy.Spider):
    name = "wangyi"
    allowed_domains = ["163.com"]
    start_urls = ["http://news.163.com"]
    analyse_html = AnalyseHtml()

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

        #提取网页中所有需要的url
        urls = self.analyse_html.GetAllUrl(response.body)
        for url in urls:
            yield Request(url, self.parse_news_page)

    def parse_news_page(self, response):
        """解析新闻正文"""
        if response.status != 200:
            self.log("get news fail:" + response.url, logging.ERROR)
            return 

        #如果网页满足新闻页格式，提取新闻内容
        ##########################
        if self.analyse_html.IsNewsUrl(response.url):
            data = NewsItem()
            data['url'] = response.url
            yield data

        #提取网页中其他需要的url
        urls = self.analyse_html.GetNewsUrl(response.body)
        for url in urls:
            yield Request(url, self.parse_news_page)

#        s_str = '<h1 id="h1title" class="ep-h1">'
#        e_str = '</h1>'
#        s = response.body.find(s_str)
#        e = response.body.find(e_str, s)
#
#        data = NewsItem()
#        data['title'] = response.body[s+len(s_str):e].decode('gb2312').encode('utf-8')
#        data['url'] = response.url
#        content = response.xpath('////div[@id="endText"]').extract_first()
#        content = self.del_main_text_mark(content)
#        data['content'] = content
#        return data

#    def del_main_text_mark(self, text):
#        """删除新闻正文无用的标签"""
#        s = text.find('<')
#        while s != -1:
#            s = text.find('<')
#            e = text.find('>', s)
#            text = text.replace(text[s:e+1], '')
#
#        text = text.replace('\n', '')
#        text = text.replace('\r', '')
#        text = text.replace(' ', '')
#        return text
