from tgi102_flask import sa, BASE, relationship, db
from sqlalchemy.sql import and_

class Category(BASE):
    __tablename__ = 'category'
    id = sa.Column(sa.String(64), primary_key=True)
    category_name = sa.Column(sa.String(64), unique=True, )

    fk_product_category = relationship('Product')

    def __repr__(self):
        return f"id={self.id}, category_name={self.category_name}"


class Mart(BASE):
    __tablename__ = 'marts'
    id = sa.Column(sa.String(64), primary_key=True)
    mart_name = sa.Column(sa.String(255), unique=True)

    fk_product_mart = relationship('Product')

    def __repr__(self):
        return f"id={self.id}, mart_name={self.mart_name}"


class Price(BASE):
    __tablename__ = 'price'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    # product_id = sa.Column(sa.Integer)
    date = sa.Column(sa.Date)
    price = sa.Column(sa.Integer)

    product_id = sa.Column(sa.Integer, sa.ForeignKey('product.id'))

    def __repr__(self):
        return f"id={self.id}, date={self.date}, price={self.price}"


class Product(BASE):
    __tablename__ = 'product'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    # mart_id = sa.Column(sa.String(64))
    # category_id = sa.Column(sa.Integer)
    product_name = sa.Column(sa.String(64))
    product_url = sa.Column(sa.String(128))
    product_pic_url = sa.Column(sa.String(256))

    fk_price = relationship('Price')

    category_id = sa.Column(sa.String(64), sa.ForeignKey('category.id'))
    mart_id = sa.Column(sa.String(64), sa.ForeignKey('marts.id'))

    def __repr__(self):
        return f"id={self.id}, product_name={self.product_name}, product_url={self.product_url}, product_pic_url={self.product_pic_url}"


def get_index_data():
    # index_sql = db.session.query(Product, Price).filter(Product.id == Price.product_id).order_by(db.func.rand()).limit(8)
    index_sql = db.session.query(Product, Price, Mart).filter(Product.id == Price.product_id).order_by(db.func.rand()).limit(8)

    index_sql_raw = """SELECT DISTINCT *  FROM (SELECT product.id, product.product_name, product.product_url, product.product_pic_url, product.mart_id, price.date, price.price FROM product JOIN price ON (product.id=price.product_id)) AS A join marts on (A.mart_id = marts.id) ORDER BY RAND() LIMIT 8"""
    index_cursor = db.session.execute(index_sql_raw)
    index_results = index_cursor.fetchall()

    index_data_list = []
    for i in index_sql:
        index_data_list.append(i)
    print("*"*100)
    print("index_data_list", index_data_list)
    print("index_results", index_results)
    print("index_results[0][0]", index_results[0][0])
    print("index_results[0][1]", index_results[0][1])
    print("index_results[0][2]", index_results[0][2])
    print("index_results[0][3]", index_results[0][3])
    print("index_results[0][5]", index_results[0][5])
    print("index_results[0][6]", index_results[0][6])
    print("index_results[0][7]", index_results[0][7])
    print("index_results[0][8]", index_results[0][8])

    return index_results


def get_count_category(category_id):
    count_category = db.session.query(db.func.count(Product.id)).filter(Product.id == Price.product_id).filter(
        Product.category_id == category_id).all()[0][0]
    return count_category


def get_category_product(category_id, end):
    category_product = db.session.query(Product, Price).filter(Product.id == Price.product_id).filter(
        Product.category_id == category_id).order_by(db.func.rand()).limit(12).offset(end)

    query_data_list = []

    for i in category_product:
        query_data_list.append(i)
    return query_data_list


def get_shop_details(product_id_query):
    shop_details = db.session.query(Product, Price).filter(Product.id == Price.product_id).filter(
        Product.id == {product_id_query}).first()

    query_data_list = []
    for i in shop_details:
        query_data_list.append(i)

    return query_data_list
