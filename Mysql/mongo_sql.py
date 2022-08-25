import pymongo
from pymongo import MongoClient
from sql_model import Mart, Product, Category, Price, BASE, Session, engine
import sqlalchemy as sa
import pandas as pd
import json
import datetime

# mongodb cloud connection
client = MongoClient('mongodb+srv://admin:tgi102aaa@cluster0.19rsmeq.mongodb.net/?retryWrites=true&w=majority')

session = Session()

date = datetime.datetime.now()
update_date = date.date()

mongo_db = client.All_Market
collections = mongo_db.PxMart
result = collections.find({'date': "2022-08-24"}, {'_id': 0}).limit(500)

# result = collections.find({'date': f'{update_date}'}, {'_id': 0}).limit(15)
result_list = []

for i in result:
    result_list.append(i)


Product_obj_list = []
price_obj_list = []

for i in result_list:
    category = i['category']
    date = i['date']
    market = i['market']
    price = i['price']
    product_name = i['product_name']
    product_url = i['product_url']
    product_pic_url = i['photos']

    Product_obj = Product(product_name=product_name, product_url=product_url, product_pic_url=product_pic_url,
                          category_id=category, mart_id=market)
    Product_obj_list.append(Product_obj)
    session.add_all(Product_obj_list)
    session.flush()
    price_obj = Price(date=date, price=price, product_id=Product_obj.id)
    price_obj_list.append(price_obj)


# select ID from

# 插入多筆數據
session.add_all(price_obj_list)
# # # # 提交數據
session.commit()
