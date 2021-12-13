import psycopg2
from flask import Flask, jsonify, g
from flask_cors import CORS, cross_origin

from model import host, user, password, db_name, get_new_product, get_category


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


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

@app.route('/', methods = ['GET'])
@cross_origin()
def index():
    return jsonify('hi dear')

@app.route('/new-product', methods = ['GET'])
@cross_origin()
def new_product():
    with  get_db().cursor() as cursor:
        return jsonify(get_new_product(cursor))

@app.route('/category', methods = ['GET'])
@cross_origin()
def category():
    with  get_db().cursor() as cursor:
        return jsonify(get_category(cursor))

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        print('close db')


if __name__ == "__main__":
    app.run(debug=True)
