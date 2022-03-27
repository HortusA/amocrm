import requests
from config import access_token
from pathlib import Path

url_company = 'https://sadovoya.amocrm.ru/api/v4/companies'
headers = {'Authorization': f"Bearer {access_token}"}

a = requests.get(url_company, headers=headers)
a = a.json()


a = a['_embedded']['companies']
col = 0
for i in a:
    try:
        Path(f"/home/hortus/Documents/bases/firms/{i['id']}").mkdir(parents=True, exist_ok=False)
    except OSError:
        print(f"Каталог с номером клиента - {i['id']} существует")
    else:
        col += 1
print(f'Создание каталогов завершено, Всего создано {col}')
