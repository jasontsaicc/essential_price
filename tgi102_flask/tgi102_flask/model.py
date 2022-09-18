from tgi102_flask import sa, BASE, relationship, db


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
    product_pic_url = sa.Column(sa.String(128))

    fk_price = relationship('Price')

    category_id = sa.Column(sa.String(64), sa.ForeignKey('category.id'))
    mart_id = sa.Column(sa.String(64), sa.ForeignKey('marts.id'))

    def __repr__(self):
        return f"id={self.id}, product_name={self.product_name}, product_url={self.product_url}, product_pic_url={self.product_pic_url}"


def get_index_data():
    index_sql = db.session.query(Product, Price).filter(Product.id == Price.product_id).order_by(db.func.rand()).limit(
        8)
    index_data_list = []
    for i in index_sql:
        index_data_list.append(i)
    return index_data_list


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
    shop_details = db.session.query(Product, Price).filter(Product.id == Price.product_id).filter(Product.id == {product_id_query}).first()

    query_data_list = []
    for i in shop_details:
        query_data_list.append(i)

    return query_data_list
