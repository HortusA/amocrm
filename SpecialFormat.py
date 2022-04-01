
from bs4 import BeautifulSoup
import pprint, re, json, sqlite3


conn = sqlite3.connect('/home/hortus/PycharmProjects/amocrm/app.db')
cursor = conn.cursor()
cursor.execute("SELECT content FROM cms_article_content limit 20")

result = cursor.fetchall()

b = []
for string in result:

    clr = re.sub(r"[\\\r\\\n]", "", string[0])
    data_string = BeautifulSoup(clr, 'lxml')

    for i in data_string.body:

        if i.name == 'p':
            b.append({'paragraph': i.text})

        elif i.name == 'figure':

            b.append({'jpeg': i.contents[0].attrs['src']})

        elif i.name == 'h2':
            b.append({'header': i.text})

        else:
            b.append({'неизвестный тег': i.text})


#j = json.dumps(b)

pprint.pprint(b)

