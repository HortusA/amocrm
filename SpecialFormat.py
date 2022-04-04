import json
import re
import sqlite3

from bs4 import BeautifulSoup

path_to_base = '/home/hortus/PycharmProjects/amocrm/app.db'


class SearchArticles:
    def __init__(self, path_to_base):
        self.conn = sqlite3.connect(path_to_base)
        self.cursor = self.conn.cursor()
        self.article_body = {}
        self.list_body = []
        self.count = 0
        self.result = None

    def execute_one(self, article_id):
        self.article_id = article_id
        self.cursor.execute("SELECT content FROM cms_article_content WHERE article_id = ?", (self.article_id,))
        self.result = self.cursor.fetchone()
        return self.result

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
        clr = re.sub(r"[\\\r\\\n]", "", content)
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
                try:
                    self.list_body.append(
                        {
                            "type": "image",
                            "data": {
                                "file": {
                                    "url": str(i.contents[0].attrs['src'])
                                },
                                "caption": "need to be correct parse",
                                "withBorder": "false",
                                "withBackground": "false",
                                "stretched": "true"
                            }
                        }
                                          )
                except IndexError:
                    print(f'отсутсвует значение{i}')
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

        return self.article_body

#j = json.dumps(list_root)


a = SearchArticles('/home/hortus/PycharmProjects/amocrm/app.db')
result = a.get_article_content()
test = a.parse_content(date=result[0], content=result[1])
print(json.dumps(test))


