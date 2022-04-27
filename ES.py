import sqlite3
import re
import requests

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
        count+=1
        clr = re.sub(r"[\\\r\\\n]", "", str(content[1]))
        data_string = BeautifulSoup(clr, 'lxml')
        for i in data_string.body:
               es.index(index='my_index', doc_type='my_index', id=count, document={'text': str(i)})


def search_id():
    es.search(index='my_index', document={'query': {'match': {'text': 'p'}}})


def get_index_es(index):
    resp = es.get(index="index", id=index)

create_index_es()
search_id()
