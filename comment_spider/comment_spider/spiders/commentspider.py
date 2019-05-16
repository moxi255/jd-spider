# -*- coding: utf-8 -*-
import scrapy
import json, re
from tools.sql_tools import *
from tools.jieba_content import get_jieba_comment
from ..items import CommentSpiderItem
from ..settings import EXISTS_CONMENTS

class CommentspiderSpider(scrapy.Spider):
    name = 'commentspider'
    allowed_domains = ['jd.com']
    start_urls = get_start_urls()


    def parse(self, response):
        if response.text:
            json_obj = json.loads(response.text)
            if json_obj:
                tag_data = json_obj['hotCommentTagStatistics']
                tags = '|'.join([tag['name'] for tag in tag_data])
                count = '|'.join([str(tag['count']) for tag in tag_data])
                url = response._url
                page_num = int(url.split('&')[4].split('=')[1])
                computer_id = int(url.split('&')[1].split('=')[1])
                comments = json_obj['comments']
                # 保存数据
                if page_num == 1:
                    save_tags(tags, count, computer_id)
                if 0 < len(comments) < 10:
                    for comment in comments:
                        comment_id = str(computer_id) + str(comment['id'])
                        content = re.sub(r"&hellip;|\.| |~|'", '', comment['content'])
                        print(content)
                        jieba_content = get_jieba_comment(content)
                        print(jieba_content)
                        create_time = comment['creationTime']
                        score = comment['score']
                        print(comment_id, content, jieba_content, score, create_time, computer_id)
                        if comment_id in EXISTS_CONMENTS:
                            print(f'{comment_id} 评论已存在')
                        else:
                            save_comment(comment_id, content, jieba_content, score, create_time, computer_id)
                    # 该商品评论爬取完成更新if_spider字段
                    update_if_spider(computer_id)

                elif len(comments) == 10:
                    for comment in comments:
                        comment_id = str(computer_id) + str(comment['id'])
                        content = comment['content'].replace(' ', '')
                        jieba_content = get_jieba_comment(content)
                        create_time = comment['creationTime']
                        score = comment['score']
                        print(comment_id, content, jieba_content, score, create_time, computer_id)
                        if comment_id in EXISTS_CONMENTS:
                            print(f'{comment_id} 评论已存在')
                        else:
                            save_comment(comment_id, content, jieba_content, score, create_time, computer_id)
                    page_num += 1
                    if page_num == 101:
                        # 该商品评论爬取完成更新if_spider字段
                        update_if_spider(computer_id)
                    # 找下一页
                    if page_num < 101:
                        next_url = f'https://club.jd.com/comment/skuProductPageComments.action?&productId={computer_id}&score=0&sortType=5&page={page_num}&pageSize=10&isShadowSku=0&rid=0&fold=1%27'
                        yield scrapy.Request(url=next_url, callback=self.parse)
                else:
                    update_if_spider(computer_id)
                    # 进行下一个商品评论收集
                    yield CommentspiderSpider()
