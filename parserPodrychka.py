import requests
import psycopg2
from bs4 import BeautifulSoup
import time

from model import host, user, password, db_name, insert_product, insert_price_list, get_product_of_category

HEADERS = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36',
           'accept': '*/*'}
HOST = 'https://www.podrygka.ru'

def get_db():
    db = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    return db

db = get_db()

categoryId = {
    'makeup': {'req': 'makiyazh', 'db': 2},
    'care': {'req': 'ukhod', 'db': 1},
    'hair': {'req': 'ukhod/volosy/', 'db': 4},
    'asia': {'req': 'ukhod/?country=republic_of_korea;thailand;japan', 'db': 5},
    'perfumer': {'req': 'parfyumeriya', 'db': 7}
}

id_store = 2

def get_html(cat, page):
    url = 'https://www.podrygka.ru/catalog/{}?PAGEN_1={}'.format(cat, page)
    r = requests.get(url, headers=HEADERS)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='item-product-card')

    products = []

    for item in items:
        title = item.find('img').get('alt').split("`", 1)
        name = ''
        volume = 0
        for i in str(title[1]).split(' '):
            if i.isdigit():
                volume = i
                break
            name += i.replace("`", "")
            name += ' '
    
        products.append(
            {
                'img': HOST + item.find('img').get('src').replace('resize_cache/', '').replace('190_190_2/', ''),
                'url': HOST + item.find_all('a')[-1].get('href'),
                'category_type': title[0],
                'name': name,
                'price': item.find('span').get_text(),
                'volume': volume
            }
        )

    return products


def parser(cat, page):
    html = get_html(cat, page)
    if html.status_code == 200:
        return get_content(html.text)
    else:
        return 404

def add_to_db(products, cat_id):
    with  db.cursor() as cursor:

        for product in products:
            response = insert_product(cursor, product['name'], product['category_type'], product['img'], (str(product['volume']).replace(',', '.') or 0), cat_id)
            db.commit()

            if response[0][0]:
                response = insert_price_list(cursor, response[0][0], id_store, product['url'], product['price'])
                db.commit()
    


for category in categoryId:
    page = 1
    cat = categoryId[category]['req']
    # count = 0
    while True:
    # while count != 10:
        time.sleep(5)
        res = parser(cat, page)
        if res == 404:
            break
        add_to_db(res, categoryId[category]['db'])
        page += 1
        # count+=1
