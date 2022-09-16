from tgi102_flask import sa, BASE, relationship
from jieba.analyse.analyzer import ChineseAnalyzer



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
    product_url = sa.Column(sa.String(64))
    product_pic_url = sa.Column(sa.String(64))

    fk_price = relationship('Price')

    category_id = sa.Column(sa.String(64), sa.ForeignKey('category.id'))
    mart_id = sa.Column(sa.String(64), sa.ForeignKey('marts.id'))


    def __repr__(self):
        return f"id={self.id}, product_name={self.product_name}, product_url={self.product_url}, product_pic_url={self.product_pic_url}"

