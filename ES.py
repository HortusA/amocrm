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

def execute_all():
    cursor.execute("SELECT content FROM cms_article_content")
    return cursor.fetchall()


def create_index_es():
    count = 0
    for content in execute_all():

        count += 1
        es.index(index='my_index', id=count, document={'text': (content)})
    print(count)

#def search_id():
 #   res = es.get(index="my_index", id=10)
 #   print(res['_source'])


def search_text():
    body = {


    }


    #resp = es.search(index="my_index", query={"match_all": {}})
    resp = es.search(index="my_index", body={'query': {'match': {'text': 'Китай'}}})

    print(resp)


create_index_es()

search_text()

