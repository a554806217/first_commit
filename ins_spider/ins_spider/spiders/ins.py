# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import Request
import re
from ..items import InsItem
class InsSpider(scrapy.Spider):
    name = 'ins'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/graphql/query/?query_hash=56066f031e6239f35a904ac20c9f37d9&variables={"id":"25025320","include_reel":false,"fetch_mutual":false,"first":24}']

    def parse(self, response):
        html = json.loads(response.text)
        end_cursor = html['data']['user']['edge_followed_by']['page_info']['end_cursor']


        all_names = html['data']['user']['edge_followed_by']['edges']
        if all_names:
            for n in all_names:
                id = n['node']['id']
                username = n['node']['username']
                url = 'https://www.instagram.com/{}/'.format(username)
                req = Request(
                    url=url,
                    callback=self.parse_detail,
                    meta={'id': id, 'username': username}
                )
                yield req

                url = 'https://www.instagram.com/graphql/query/?query_hash=56066f031e6239f35a904ac20c9f37d9&variables={"id":"%s","include_reel":false,"fetch_mutual":false,"first":24}'%id
                yield Request(url=url, callback=self.parse)

        url = 'https://www.instagram.com/graphql/query/?query_hash=56066f031e6239f35a904ac20c9f37d9&variables={"id":"25025320","include_reel":false,"fetch_mutual":false,"first":12,"after":"%s"}' % (end_cursor)
        yield Request(url=url, callback=self.parse)


    def parse_detail(self,response):

        pattern = re.compile(r'<script type="text/javascript">window._sharedData = (.*?);</script>', re.S)
        res = re.findall(pattern, response.text)[0]
        html = json.loads(res)

        metas = html['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
        if metas:
            for m in metas:
                if m['node']['display_url']:
                    shortcode = m['node']['shortcode']
                    username = response.meta.get('username')
                    id = response.meta.get('id')
                    url = 'https://www.instagram.com/p/{}/?taken-by={}'.format(shortcode, username)
                    req = Request(
                        url=url,
                        callback=self.parse_s_detail,
                        meta={'id': id, 'username': username}

                                  )
                    yield req
        else:
            print('该用户为隐私用户，请关注后再进行获取...')

        has_next_page = html['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
        if has_next_page:
            # 下一页code
            end_cursor = html['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
            id = response.meta.get('id')
            username = response.meta.get('username')
            # 拼接完整 url地址
            url = 'https://www.instagram.com/graphql/query/?query_hash=a5164aed103f24b03e7b7747a2d94e3c&variables={"id":"%s","first":12,"after":"%s"}' % (id, end_cursor)

            yield scrapy.Request(
                url=url,
                meta={'id': id, 'username': username},
                callback=self.parse_json_data
            )

    def parse_json_data(self, response):
        # 返回的是json数据,解析用户主页下一页数据
        js_data = json.loads(response.text)
        if js_data:
            if js_data['data']['user']:
                edges = js_data['data']['user']['edge_owner_to_timeline_media']['edges']

                if edges:

                    for edge in edges:
                        # 判断是否为视频
                        if edge['node']['display_url']:
                            username = response.meta.get('username')
                            id = response.meta.get('id')
                            # 详情页面code
                            shortcode = edge['node']['shortcode']

                            # 拼接详情url
                            url = 'https://www.instagram.com/p/{}/?taken-by={}'.format(shortcode, username)
                            yield scrapy.Request(
                                url=url,
                                meta={
                                    'id': id, 'username': username
                                },
                                callback=self.parse_s_detail
                            )

            # 解析下一页
            has_next_page = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
            if has_next_page:
                # 下一页code
                end_cursor = js_data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
                id = response.meta.get('id')
                username = response.meta.get('username')
                # 拼接完整 url地址
                url = 'https://www.instagram.com/graphql/query/?query_hash=a5164aed103f24b03e7b7747a2d94e3c&variables={"id":"%s","first":12,"after":"%s"}' % (
                id, end_cursor)

                yield scrapy.Request(
                    url=url,

                    meta={
                        'id': id, 'username':username
                    },
                    callback=self.parse_json_data
                )




    def parse_s_detail(self,response):
        username = response.meta.get('username')
        id = response.meta.get('id')
        pattern = re.compile(r'<script type="text/javascript">window._sharedData = (.*?);</script>', re.S)
        res = re.findall(pattern, response.text)[0]
        html = json.loads(res)
        article_id = html['entry_data']['PostPage'][0]['graphql']['shortcode_media']['id']
        img_src = html['entry_data']['PostPage'][0]['graphql']['shortcode_media']['display_url']
        try:
            content =html['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_to_caption']['edges'][0]['node']['text']
        except Exception as e:
            content = ''
        com_edges = html['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_to_comment']['edges']
        if com_edges:
            # 拼接评论
            comments = ';'.join([c['node']['text'] for c in com_edges])

        else:

            comments = '无'

        item = InsItem()
        item['id'] = id
        item['article_id'] = article_id
        item['username'] = username
        item['content'] = content
        item['comments'] = comments
        item['img_src'] = [img_src]
        yield item