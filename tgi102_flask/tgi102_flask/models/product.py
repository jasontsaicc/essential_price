from tgi102_flask import sa, BASE, relationship
from jieba.analyse.analyzer import ChineseAnalyzer
import flask_whooshalchemyplus
from tgi102_flask import app

class Product(BASE):
    __tablename__ = 'product'
    # flask_whooshalchemy
    __searchable__ = ['product_name']
    __analyzer__ = ChineseAnalyzer()


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

