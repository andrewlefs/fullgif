from apps.posts.models import Post
from bs4 import BeautifulSoup
from urllib import parse
import json
import requests
import logging
import traceback

logger = logging.getLogger(__name__)


class AutoFull(object):
    def __init__(self):
        self.cur_post = 0
        self.load_more_url = "http://9gag.com//gif?id=a9PGerj%2Cam8Zy86%2CazVp8LK&c=5998"
        self.request = requests.session()

    def run(self):
        if not self.load_more_url:
            url_next = self.get_home_page()
        else:
            url_next = self.load_more_url

        if url_next:
            next_data = self.get_next_page(url_next)
            if next_data:
                self.parse_data(next_data)

    def get_home_page(self):
        try:
            body = self.request.get('http://9gag.com/gif')
            if body.status_code == 200:
                html = BeautifulSoup(body.text)
                url_next = html.find('a', {'class': 'btn badge-load-more-post'}).attrs['href']
                url_next = parse.unquote(url_next, encoding='utf-8', errors='replace')
                return "http://9gag.com/" + url_next
            return False
        except:
            print(traceback.format_exc())
            logger.error(traceback.format_exc())
            return False

    def get_next_page(self, url_next):
        try:
            headers = {
                "Host": "9gag.com",
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "http://9gag.com/gif",
                "Connection": "keep-alive",
                "X-Requested-With": "XMLHttpRequest",
                "Connection": "keep-alive",
            }
            body = self.request.get(url_next, headers=headers)
            if body.status_code == 200:
                data = json.loads(body.text)
                return data
            return False
        except:
            print(traceback.format_exc())
            logger.error(traceback.format_exc())
            return False

    def parse_data(self, data):
        try:
            obj_save = {
                'name': '',
                'slug': '',
                'parent': '',
                'webm': '',
                'mp4': '',
                'image': '',
            }
            if data['okay']:
                for key, value in data['items'].items():
                    html = BeautifulSoup(value)
                    try:
                        obj_save['parent'] = key
                        obj_save['name'] = html.find('h2', {'class': 'badge-item-title'}).text.strip()
                        obj_save['image'] = html.find('img', {'class': 'badge-item-img'}).attrs['src'].strip()
                        sources = html.find_all('source')
                        for source in sources:
                            src = source.attrs['src']
                            if 'mp4' in src:
                                obj_save['mp4'] = src
                            elif 'webm' in src:
                                obj_save['webm'] = src

                        # Save to database
                        if not Post.objects.filter(parent=obj_save['parent']).exists():
                            Post.objects.create(name=obj_save['name'], slug='', parent=obj_save['parent'],
                                                webm=obj_save['webm'], mp4=obj_save['mp4'], image=obj_save['image'])
                        else:
                            print('Have some data exits: ', obj_save)
                    except:
                        print('Some parse data error: ', data)
                        print(traceback.format_exc())
                        logger.error(traceback.format_exc())

                # Get data success
                if data['loadMoreUrl']:
                    self.cur_post += len(data['ids'])
                    self.load_more_url = "http://9gag.com/" + data['loadMoreUrl']

                    print('Count request posts gif: ', str(self.cur_post))
                    print('Last url: ', self.load_more_url)

                    self.run()
                else:
                    print(data)
        except:
            print('Data error: ', data)
            print(traceback.format_exc())
            logger.error(traceback.format_exc())


class AutoNews(object):
    def __init__(self):
        self.request = requests.session()

    def run(self):
        article = self.get_home_page()

        if article:
            self.parse_data(article)

    def get_home_page(self):
        try:
            body = self.request.get('http://9gag.com/gif')
            if body.status_code == 200:
                html = BeautifulSoup(body.text)
                articles = html.find_all('article')
                return articles
            return False
        except:
            print(traceback.format_exc())
            logger.error(traceback.format_exc())
            return False

    def parse_data(self, data):
        try:
            obj_save = {
                'name': '',
                'slug': '',
                'parent': '',
                'webm': '',
                'mp4': '',
                'image': '',
            }
            for value in data:
                html = BeautifulSoup(str(value))
                try:
                    obj_save['parent'] = html.find('article').attrs['data-entry-id']
                    obj_save['name'] = html.find('h2', {'class': 'badge-item-title'}).text.strip()
                    obj_save['image'] = html.find('img', {'class': 'badge-item-img'}).attrs['src'].strip()
                    sources = html.find_all('source')
                    for source in sources:
                        src = source.attrs['src']
                        if 'mp4' in src:
                            obj_save['mp4'] = src
                        elif 'webm' in src:
                            obj_save['webm'] = src

                    # Save to database
                    if not Post.objects.filter(parent=obj_save['parent']).exists():
                        Post.objects.create(name=obj_save['name'], slug='', parent=obj_save['parent'],
                                            webm=obj_save['webm'], mp4=obj_save['mp4'], image=obj_save['image'])
                    else:
                        print('Have some data exits: ', obj_save)
                except:
                    print('Some parse data error: ', data)
                    print(traceback.format_exc())
                    logger.error(traceback.format_exc())
        except:
            print('Data error: ', data)
            print(traceback.format_exc())
            logger.error(traceback.format_exc())
