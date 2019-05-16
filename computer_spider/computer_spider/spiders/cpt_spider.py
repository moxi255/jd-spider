# -*- coding: utf-8 -*-
import scrapy
import json, re
from ..items import ComputerSpiderItem

class CptSpiderSpider(scrapy.Spider):
    name = 'cpt_spider'
    allowed_domains = ['jd.com', 'p.3.cn']
    start_urls = ['https://list.jd.com/list.html?cat=670%2C671%2C672']

    def parse(self, response):
        """
        获取京东笔记本各大品牌的url
        :param response:
        :return:
        """
        brand_urls = response.xpath('//ul[@id="brandsArea"]/li/a/@href').extract()
        brands = response.xpath('//ul[@id="brandsArea"]/li/a/@title').extract()
        print(len(brand_urls), len(brands))
        for index, brand_url in enumerate(brand_urls):
            brand_url = 'https://list.jd.com' + brand_url
            brand = brands[index]
            print(brand)
            if '华为' in brand:
                brand = 'huawei'
            elif '联想' in brand:
                brand = 'Lenovo'
            elif 'ThinkPad' in brand:
                brand = 'ThinkPad'
            elif 'Apple' in brand:
                brand = 'apple'
            elif '戴尔' in brand:
                brand = 'DELL'
            elif '三星' in brand:
                brand = 'samsung'
            elif '华硕' in brand:
                brand = 'ASUS'
            elif '惠普' in brand:
                brand = 'HP'
            elif '宏碁' in brand:
                brand = 'acer'
            elif '小米' in brand:
                brand = 'xiaomi'
            elif '微软' in brand:
                brand = 'Microsoft'
            elif '外星人' in brand:
                brand = 'Alienware'
            elif '机械革命' in brand:
                brand = 'MECHREVO'
            elif '神舟' in brand:
                brand = 'HASEE'
            elif '微星' in brand:
                brand = 'MSI'
            elif '雷蛇' in brand:
                brand = 'Razer'
            elif '戴睿' in brand:
                brand = 'dere'
            elif '海尔' in brand:
                brand = 'Haier'
            response.meta['brand'] = brand
            print(brand)
            yield scrapy.Request(url=brand_url, callback=self.parse_list_page, meta=response.meta)

    def parse_list_page(self, response):
        """
        解析列表页
        :param response:
        :return:
        """
        detail_urls = response.xpath('//li[@class="gl-item"]/div/div[@class="p-img"]/a/@href').extract()
        src_img_urls = response.xpath(
            '//li[@class="gl-item"]/div/div[@class="p-img"]/a[@target="_blank"]/img/@src').extract()
        data_lazy_img_urls = response.xpath(
            '//li[@class="gl-item"]/div/div[@class="p-img"]/a[@target="_blank"]/img/@data-lazy-img').extract()
        img_urls = src_img_urls + data_lazy_img_urls
        next_url = response.xpath('//a[contains(text(), "下一页")]/@href').extract_first()
        print(len(detail_urls), len(img_urls))
        for index, detail_url in enumerate(detail_urls):
            detail_url = 'https:' + detail_url
            goods_id = detail_url.split('/')[-1].split('.')[0]
            response.meta['goods_id'] = goods_id
            img_url = 'https:' + img_urls[index]
            response.meta['img_url'] = img_url
            yield scrapy.Request(url=detail_url, callback=self.parse_detail_page, meta=response.meta)
        if next_url:
            next_url = 'https://list.jd.com' + next_url
            yield scrapy.Request(url=next_url, callback=self.parse_list_page, meta=response.meta)

    def parse_detail_page(self, response):
        """
        解析详情页
        :param response:
        :return:
        """
        title = response.xpath('//title/text()').extract_first()
        title = re.sub('【.*?】|-京东', '', title.strip())
        print(title)
        param = response.xpath('//div[@class="Ptable"]').extract()
        if len(param):
            param = param[0]
        else:
            param = response.xpath('//table[@class="Ptable"]').extract()[0]
        # 处理参数
        param = re.sub('  |\t|\r|\n', '', param)
        # print(param)
        response.meta['title'] = title
        response.meta['param'] = param
        price_url = 'https://p.3.cn/prices/mgets?skuIds=J_' + response.meta['goods_id']
        yield scrapy.Request(url=price_url, callback=self.get_goods_price, meta=response.meta)

    def get_goods_price(self, response):
        """
        获取商品价格
        :param response:
        :return:
        """
        json_obj = json.loads(response.text)
        price = json_obj[0]['p']
        response.meta['price'] = price
        item = ComputerSpiderItem()
        item['goods_id'] = int(response.meta['goods_id'])
        item['brand'] = response.meta['brand']
        item['title'] = response.meta['title']
        item['img_url'] = response.meta['img_url']
        item['param'] = response.meta['param']
        item['price'] = response.meta['price']
        yield item
