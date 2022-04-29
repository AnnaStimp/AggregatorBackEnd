from ast import Str
import psycopg2
import requests
import json

from model import host, user, password, db_name, insert_product

categoryId = {
    'makeup': 3,
    'care': 4,
    'pharmacy': 3747,
    'hair': 6,
    'asia': 10,
    'organic': 12,
    'perfumer': 7
}

def get_db():
    db = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    return db

url = 'https://goldapple.ru/web_scripts/discover/category/products?cat=3&page=1'

headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36',
           'accept': '*/*'}

r = requests.get(url, headers=headers)
pr = json.loads(r.text)['products']

db = get_db()

for i in pr:
    with  db.cursor() as cursor:
        name = str(i['brand']).upper() + str(i['name']).lower()
        response = insert_product(cursor, name, i['category_type'], i['url'], 2)
        db.commit()
        print(response[0][0])














import requests
# from bs4 import BeautifulSoup

# url = 'https://goldapple.ru/uhod'

# headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36',
#            'accept': '*/*'}

# def get_html(url, params=None):
#     r = requests.get(url, headers=headers, params=params)
#     return r

# def get_content(html):
#     # print(html)
#     soup = BeautifulSoup(html, 'html.parser')
#     items = soup.find_all(class_='catalog-products')
#     print(items)

# def parser():
#     html = get_html(url)
#     if html.status_code == 200:
#         get_content(html.text)
#     else:
#         'ere'


# parser()
