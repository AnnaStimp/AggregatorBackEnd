import psycopg2
from flask import Flask, jsonify, g
from flask_cors import CORS, cross_origin

from model import host, user, password, db_name, get_new_product, get_category, get_product_of_category, get_product, get_products


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# функция подключения к базе данных и сохранение адреса в переменную
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
    return db

@app.route('/', methods = ['GET']) # создание базового пути
@cross_origin()
def index():
    return jsonify('hi dear')

@app.route('/new-product', methods = ['GET']) # создание пути для получения данных о новинках
@cross_origin()
def new_product():
    with  get_db().cursor() as cursor:
        response = get_new_product(cursor)
        if len(response) == 0:
            return page_not_found('Not found new products')

        return jsonify(response)

@app.route('/category', methods = ['GET']) # создание пути для получения данных о категориях
@cross_origin()
def category():
    with  get_db().cursor() as cursor:
        response = get_category(cursor)
        if len(response) == 0:
            return page_not_found('Not found categorys')
            
        return jsonify(response)

@app.route('/category/<category_id>', methods = ['GET']) # создание пути для получения данных о товарах конркетной категории
def product_of_category(category_id):
    with  get_db().cursor() as cursor:
        response = get_product_of_category(cursor, category_id)
        if len(response) == 0:
            return page_not_found(f'Not found products of category {category_id}')
            
        return jsonify(response)

@app.route('/product', methods = ['GET']) # создание пути для получения всех id товаров
def products():
    with  get_db().cursor() as cursor:
        response = get_products(cursor)
        if len(response) == 0:
            return page_not_found('Not found products')
            
        return jsonify(response)

@app.route('/product/<product_id>', methods = ['GET']) # создание пути для получения данных о конкретном товаре
def product(product_id):
    with  get_db().cursor() as cursor:
        response = get_product(cursor, product_id)
        if len(response) == 0:
            return page_not_found(f'Not found products {product_id}')
            
        return jsonify(response)

@app.teardown_appcontext # функция, закрывающая базу данных, когда приложение перестает работать
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        print('close db')

@app.errorhandler(404)
def page_not_found(mes):
    return {'status': 404, 'message': f'{mes}'}, 404

if __name__ == "__main__":
    app.run(debug=True)
