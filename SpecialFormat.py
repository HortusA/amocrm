
from bs4 import BeautifulSoup
import pprint, re
import sqlite3


conn = sqlite3.connect('/home/hortus/PycharmProjects/amocrm/app.db')
cursor = conn.cursor()
cursor.execute("SELECT content FROM cms_article_content ")
result = cursor.fetchall()

for r in result:

    b = []
    all_doc = BeautifulSoup(r, 'lxml')
    for i in all_doc.body:
        if i.name == 'p':
            clr = re.sub(r"[\r\n\\r\\n]", "", i.text)
            b.append({'paragraph' : clr})
        elif i.name == 'figure':
            b.append({'jpeg': i})
        else:
            clr = re.sub(r"[\r\n\\r\\n]", "", i)
            b.append({'неизвестный тег': clr})


pprint.pprint(b)
conn.close()

