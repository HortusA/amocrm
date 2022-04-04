
from bs4 import BeautifulSoup
import pprint, re, json, sqlite3

path_to_base = '/home/hortus/PycharmProjects/amocrm/app.db'



class SearchArticles:

    def __init__(self, path_to_base):
        self.conn = sqlite3.connect(path_to_base)
        self.cursor = self.conn.cursor()
        self.list_root = []
        self.list_body = []
        self.count = 0

    def execute_one(self, article_id):
        self.cursor.execute("SELECT content FROM cms_article_content WHERE article_id = ?", (article_id,))
        self.result = self.cursor.fetchone()
        return self.result

    def execute_all(self,):
        self.cursor.execute("SELECT content FROM cms_article_content")
        self.result = self.cursor.fetchall()
        return self.result

    def exrcute_metod(self, method):
        self.result = method
        for string in self.result:
            self.count += 1
            clr = re.sub(r"[\\\r\\\n]", "", string)
            data_string = BeautifulSoup(clr, 'lxml')

            for i in data_string.body:

                if i.name == 'p':
                    self.list_body.append({f'"type" :paragraph': i.text})

                elif i.name == 'figure':
                    try:
                        self.list_body.append({f'"type" :jpeg"': str(i.contents[0])})
                    except IndexError:
                        print(f'отсутсвует значение{i}')
                elif i.name == 'h2':
                    self.list_body.append({f'"type" :h2': i.text})

                else:
                    self.list_body.append({f'"type" :unknown tag': i.text})

            self.list_root.append({f' Number {self.count},"blocks"': self.list_body})

        pprint.pprint(self.list_root)

#j = json.dumps(list_root)


a=SearchArticles('/home/hortus/PycharmProjects/amocrm/app.db')
a.exrcute_metod(a.execute_one(10))

