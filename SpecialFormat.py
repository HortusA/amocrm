
from bs4 import BeautifulSoup
import pprint, re
import sqlite3


conn = sqlite3.connect('/home/hortus/PycharmProjects/amocrm/app.db')
cursor = conn.cursor()
cursor.execute("SELECT content FROM cms_article_content ")
result = cursor.fetchall()

b = []
for string in result:


    clr = re.sub(r"[\r\n\\r\\n]", "", string[0])
    data_string = BeautifulSoup(clr, 'lxml')

    for i in data_string.body:

        if i.name == 'p':
            b.append({'paragraph': i.text})
        elif i.name == 'figure':
            b.append({'jpeg': i})
        else:
            b.append({'неизвестный тег': i})


pprint.pprint(b)
conn.close()