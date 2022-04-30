import requests
from elasticsearch import Elasticsearch

es = Elasticsearch()



url = '192.168.0.111:9200'

id = {
    "title": 'product',
    "category": 'patent'
}


a= requests.put(url, json=id)
print(a.json())

