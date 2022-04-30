import psycopg2
import requests
import json

from model import host, user, password, db_name, insert_product, insert_price_list

categoryId = {
    'makeup': {'req': 3, 'db': 2},
    'care': {'req': 4, 'db': 1},
    'pharmacy': {'req': 3747, 'db': 3},
    'hair': {'req': 6, 'db': 4},
    'asia': {'req': 10, 'db': 5},
    'organic': {'req': 12, 'db': 6},
    'perfumer': {'req': 7, 'db': 7}
}

id_store = 1

HEADERS = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36',
           'accept': '*/*'}

def get_db():
    db = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    return db

db = get_db()

for category in categoryId:
    page = 1
    cat = categoryId[category]['req']

    url = 'https://goldapple.ru/web_scripts/discover/category/products?cat={}&page={}'.format(cat, page)
    r = requests.get(url, headers=HEADERS)
    result_of_req = json.loads(r.text)

    while 'products' in result_of_req.keys():
        products = result_of_req['products']

        for i in products:
            with  db.cursor() as cursor:
                name = '{} {}'.format(str(i['brand']).upper().replace(r"'", ""), str(i['name']).lower().replace(r"'", ""))
                response = insert_product(cursor, name, i['category_type'], i['webp_image_url'], categoryId[category]['db'])
                db.commit()

                if response[0][0]:
                    response = insert_price_list(cursor, response[0][0], id_store, i['url'], i['price'])
                    db.commit()
        
        page+=1
        url = 'https://goldapple.ru/web_scripts/discover/category/products?cat={}&page={}'.format(cat, page)
        r = requests.get(url, headers=HEADERS)
        result_of_req = json.loads(r.text)

print('end')

# import requests
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
