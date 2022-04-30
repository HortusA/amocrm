import sqlite3
import re
import requests
import datetime

from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch

es = Elasticsearch('http://192.168.0.111:9200')


path_to_base = '/home/alex/Документы/amocrm/app.db'
conn = sqlite3.connect(path_to_base)
cursor = conn.cursor()
list_body = []


def get_article_all():
        cursor.execute("""SELECT a.date, ac.content FROM cms_article_content ac
                                LEFT JOIN cms_articles a on a.article_id = ac.article_id
                                WHERE a.article_id""")
        return cursor.fetchall()


def create_index_es():
    count = 0
    for content in get_article_all():
        count += 1

        es.index(index='my_index', id=count, document={'text': str(content)})


def search_id():
    res = es.get(index="my_index", id=10)
    print(res['_source'])


def search_text():
    resp = es.search(index="my_index", query={"match_all": {}})
    print("Got %d Hits:" % resp['hits']['total']['value'])
    for hit in resp['hits']['hits']:
        print(hit["_source"])


create_index_es()
search_id()
search_text()

