host = '127.0.0.1'
user = 'postgres'
password = 'AnnaStimp13'
db_name = 'aggregator'
port = 5432
    

def get_new_product (cursor):
  cursor.execute(
    """SELECT product.id_product, product.name_product, product.about_product,
    MIN(price) AS price, picture_product
    FROM price_list INNER JOIN product
    ON product.ID_product = price_list.ID_product
    GROUP BY product.name_product, product.about_product, picture_product, product.id_product
    ORDER BY product.id_product DESC
    limit 4"""
  )

  return cursor.fetchall()

def get_category (cursor):
  cursor.execute(
    """SELECT *
    FROM category"""
  )

  return cursor.fetchall()