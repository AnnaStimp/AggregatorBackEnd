# данные для подключения к базе данных
host = '127.0.0.1'
user = 'postgres'
password = 'AnnaStimp13'
db_name = 'aggregator'
port = 5432
    
# функция для получения последних шестнадцати добавленных товаров в базу данных
def get_new_product (cursor):
  cursor.execute(
    """SELECT product.id_product, product.name_product, product.about_product,
    MIN(price)::money::numeric::float8 AS price, picture_product
    FROM price_list INNER JOIN product
    ON product.ID_product = price_list.ID_product
    GROUP BY product.name_product, product.about_product, picture_product, product.id_product
    ORDER BY product.id_product DESC
    limit 16"""
  )

  return cursor.fetchall()

# функция для получения информации о категориях товаров из базы данных
def get_category (cursor):
  cursor.execute(
    """SELECT *
    FROM category"""
  )

  return cursor.fetchall()

# функция для получения информации о товарах конкретной категории из базы данных
def get_product_of_category (cursor, id):
  cursor.execute(
    """SELECT product.id_category, product.id_product, product.name_product, product.about_product,
    MIN(price)::money::numeric::float8 AS price, picture_product, viewing
    FROM price_list INNER JOIN product
    ON product.ID_product = price_list.ID_product
    WHERE product.id_category = {}
    GROUP BY product.name_product, product.about_product, picture_product, product.id_product""".format(id)
  )

  return cursor.fetchall()

# функция для получения информации о товаре из базы данных
def get_product (cursor, id):
  cursor.execute(
    """SELECT product.id_product, product.name_product, store.name_store, product.about_product, price::money::numeric::float8, link_product, picture_product
    FROM price_list INNER JOIN product 
    ON product.id_product = price_list.id_product INNER JOIN store
    ON store.id_store = price_list.id_store
    WHERE product.id_product = {}""".format(id)
  )

  return cursor.fetchall()

# функция для получения id товаров из базы данных
def get_products (cursor):
  cursor.execute(
    """SELECT id_product
    FROM product"""
  )

  return cursor.fetchall()

# # функция для внесения данных о товаре в базу данных
# def insert_product (cursor, name, about, url, volume, id_category):
#   cursor.execute(
#     """INSERT INTO product (name_product, about_product, picture_product, volume, id_category)
#         VALUES ('{}', '{}', '{}', '{}', {})
#         RETURNING id_product;""".format(name, about, url, volume, id_category)
#   )

#   return cursor.fetchall()

# # функция для внесения данных в прайс-лист конкретного товара в базу данных
# def insert_price_list (cursor, id_product, id_store, link_product, price):
#   cursor.execute(
#     """INSERT INTO price_list (id_product, id_store, link_product, price)
#         VALUES ({}, {}, '{}', {});""".format(id_product, id_store, link_product, price)
#   )

#   return cursor.statusmessage

# функция для обновления информации о просмотре товара в базе данных
def product_viewing (cursor, id_product):
  cursor.execute(
    """UPDATE product
      SET viewing = viewing+1 
      WHERE id_product = {};""".format(id_product)
  )

  return cursor.statusmessage