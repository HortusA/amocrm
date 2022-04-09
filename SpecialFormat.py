import json
import re
import sqlite3
from bs4 import BeautifulSoup
import pprint
import urllib.parse
import requests

path_to_base = '/home/hortus/PycharmProjects/amocrm/app.db'


class SearchArticles:
    def __init__(self, path_to_base):
        self.conn = sqlite3.connect(path_to_base)
        self.cursor = self.conn.cursor()
        self.article_body = {}
        self.list_body = []
        self.count = 0
        self.result = None
        self.protocol=[]
        self.jpg_list = []
        self.url_error = []

    def execute_one(self, article_id):
        self.article_id = article_id
        self.cursor.execute("SELECT content FROM cms_article_content WHERE article_id = ?", (self.article_id,))
        self.result = self.cursor.fetchone()
        return self.result

    def get_article_all(self):
        self.cursor.execute("""SELECT a.date, ac.content FROM cms_article_content ac
                                LEFT JOIN cms_articles a on a.article_id = ac.article_id
                                WHERE a.article_id""")
        return self.cursor.fetchall()

    def list_img(self):
        pass

    def execute_all(self,):
        self.cursor.execute("SELECT content FROM cms_article_content")
        self.result = self.cursor.fetchall()
        return self.result

    def get_article_content(self):
        self.cursor.execute("""SELECT a.date, ac.content FROM cms_article_content ac
                                LEFT JOIN cms_articles a on a.article_id = ac.article_id
                                WHERE a.article_id = 7""")
        return self.cursor.fetchone()

    def parse_content(self, date, content):
        for content in self.get_article_all():
            clr = re.sub(r"[\\\r\\\n]", "", str(content[1]))
            data_string = BeautifulSoup(clr, 'lxml')

            for i in data_string.body:
                if i.name == 'p':
                    self.list_body.append({
                            "type": "paragraph",
                            "data": {
                                "text": str(i.text),
                                }
                    })
                elif i.name == 'figure':

                    caption = (i.find('figcaption'))
                    if caption is not None:
                        print(caption.text, '_______________________________________')
                    if i.contents and 'src' in i.contents[0].attrs:
                        url = (str(i.contents[0].attrs['src']))
                        clear_url = urllib.parse.urlsplit(url)
                        if clear_url.netloc == "onlinepatent.ru":
                            with requests.get(url, stream=True) as r:
                                r.raise_for_status()
                                count = 0
                                for chunk in r.iter_content(chunk_size=256):
                                    chunk = chunk
                                    if chunk:
                                        count += 1
                                        print(count)
                                    return 'ok'


                                print(r.iter_content)
                                self.protocol.append(str(i.contents[0].attrs['src']))

                                self.list_body.append(
                                    {
                                        "type": "image",
                                        "data": {
                                            "file": {

                                                "url": str(i.contents[0].attrs)
                                            },
                                            "caption": "need to be correct parse",
                                            "withBorder": "false",
                                            "withBackground": "false",
                                            "stretched": "true"
                                        }
                                    }
                                              )

                            self.url_error.append(i)
                    else:

                        self.url_error.append(i)


                elif i.name == 'h2':
                    self.list_body.append(
                            {
                                "type": "header",
                                "data": {
                                    "text": str(i.text),
                                    "level": 2
                                }
                            }
                    )


                elif i.name == 'н':
                    print('figcaption')

                else:
                    #self.list_body.append({f'"type" :unknown tag': i.text})
                    pass

            self.article_body.update(
                {
                    "time":  date,
                    "blocks": self.list_body,
                    "version": "0.01"
                 }
            )


            with open('rep.html', 'w') as File:
                File.write('<html>')
                File.write('<body>')
                File.write('<table>')

                for i in self.protocol:
                    File.write(f'<p> {i} </p>')

                File.write('</table>')
                File.write('</body>')
                File.write('</html>')

            with open('rep_eroros.html', 'w') as File:
                File.write('<html>')
                File.write('<body>')
                File.write('<table>')

                for i in self.url_error:
                    File.write(f'<p> {i} </p>')

                File.write('</table>')
                File.write('</body>')
                File.write('</html>')

        pprint.pprint(self.url_error)
        return self.article_body



#urlretrieve(url, file_path)
a = SearchArticles('/home/hortus/PycharmProjects/amocrm/app.db')
result = a.get_article_content()
test = a.parse_content(date=result[0], content=result[1])

print(json.dumps(test))
