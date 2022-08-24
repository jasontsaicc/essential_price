import pymongo
from pymongo import MongoClient
import datetime

client = MongoClient('mongodb+srv://admin:<password>@cluster0.19rsmeq.mongodb.net/?retryWrites=true&w=majority')

db = client.All_Market
collections = db.productions

# insert
# product = {'Category': 'rice_oil_powder', 'Date': '2022-08-24', 'Market': 'pxgo',  'Price': '89', 
# 'Product_name': '【一次取】馬玉山黑芝麻糊30gx12入', 'Url': 'https://shop.pxmart.com.tw/SalePage/Index/2448515'}

# data = collections.insert_one(product)
# print(data)

# find
date = datetime.datetime.now()
update_date = date.date()
# print(update_date)
result = collections.find({'Date': f'{update_date}'}, {'_id':0})

for i in result:
    # print(type(i)) # 回傳結果是dic類型
    print(i)
