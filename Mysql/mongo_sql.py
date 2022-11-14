import pymongo
from pymongo import MongoClient
from sql_model import Mart, Product, Category, Price, BASE, Session, engine
import sqlalchemy as sa
import pandas as pd
import json
import time

session = Session()
# date = time.strftime("%Y-%m-%d")
date = "2022-09-23"


# mongodb cloud connection
client = MongoClient('mongodb+srv://admin:00065638@serverlessinstance0.yltvt.mongodb.net')

session = Session()

date = datetime.datetime.now()
update_date = date.date()

mongo_db = client.All_Market
collections = mongo_db.PxMart2
result = collections.find({'date': "2022-11-13"}, {'_id': 0})

# result = collections.find({'date': f'{update_date}'}, {'_id': 0}).limit(15)
result_list = []

for i in result:
    result_list.append(i)


market_list = ["PxMart2","Carrefour","RT-Mart"]
for i in market_list:
    result_list = []
    collections = mongo_db[i]
    result = collections.find({'date': f"{date}"}, {'_id': 0})
    for j in result:
        result_list.append(j)

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

        Product_obj = Product(product_name=product_name,
            product_url=product_url,
            product_pic_url=product_pic_url,
            category_id=category,
            mart_id=market)
        Product_obj_list.append(Product_obj)
        session.add_all(Product_obj_list)
        session.flush()

        price_obj = Price(date=date,
            price=price,
            product_id=Product_obj.id)
        price_obj_list.append(price_obj)

    # 插入多筆數據
    session.add_all(price_obj_list)
    # 提交數據
    session.commit()
