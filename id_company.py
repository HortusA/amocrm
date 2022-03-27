import requests
from config import access_token
from pathlib import Path

url_company = 'https://sadovoya.amocrm.ru/api/v4/companies'
headers = {'Authorization': f"Bearer {access_token}"}


class IdCompany:
    def __init__(self, url=url_company, header=headers):
        self.url = url
        self.headers = header
        self.response = None
        self.result = None

    def amo_data(self):
        self.response = requests.get(self.url, headers=self.headers)
        return self.response

    def getting_data(self):
        if self.amo_data().status_code == 200:
            self.result = self.amo_data().json()
            return self.result
        else:
            return 'Дотсупа нет'

    def show_status_cod(self):
        print(self.amo_data().status_code)


class Dir:
    def __init__(self, company, col=0):
        self.company = company
        self.col = col

    def show_id(self):
        data_dict = self.company['_embedded']['companies']
        col = 0
        for i in data_dict:
            try:
                Path(f"/home/hortus/Documents/bases/firms/{i['id']}").mkdir(parents=True, exist_ok=False)
            except OSError:
                print(f"Каталог с номером клиента - {i['id']} существует")
            else:
                col += 1
        print(f'Создание каталогов завершено, Всего создано {col}')

        
a = IdCompany()
a.show_status_cod()
b = Dir(a.access_data())
b.show_id()



