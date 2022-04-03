
from bs4 import BeautifulSoup
import pprint, re, json, sqlite3


conn = sqlite3.connect('/home/hortus/PycharmProjects/amocrm/app.db')
cursor = conn.cursor()
cursor.execute("SELECT content FROM cms_article_content limit 3")

result = cursor.fetchall()
list_root = []
list_body = []
coun = 0


for string in result:
    coun =+ 1

    clr = re.sub(r"[\\\r\\\n]", "", string[0])
    data_string = BeautifulSoup(clr, 'lxml')

    for i in data_string.body:

        if i.name == 'p':
            list_body.append({f'"type" :paragraph': i.text})

        elif i.name == 'figure':
                if str(i.contents[0]) != 'None':
                    list_body.append({f'"type" :jpeg"': str(i.contents[0])})


        elif i.name == 'h2':
            list_body.append({f'"type" :h2': i.text})

        else:
            list_body.append({f'"type" :unknown tag': i.text})

    list_root.append({f' Number {coun},"blocks"': list_body})
j = json.dumps(list_root)

pprint.pprint(list_root)

