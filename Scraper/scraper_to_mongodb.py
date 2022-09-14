import pymongo
from pymongo import MongoClient
import datetime


client = MongoClient(host="localhost", port=27017)
db = client.admin
collection = db['test']
# client = MongoClient('mongodb+srv://admin:tgi102aaa@cluster0.19rsmeq.mongodb.net/?retryWrites=true&w=majority')
# db = client.All_Market

# test data
# product = [{'Category': 'rice_oil_powder', 'Date': '2022-08-24', 'Market': 'pxgo',  'Price': '89', 
# 'Product_name': '【一次取】馬玉山黑芝麻糊30gx12入', 'Url': 'https://shop.pxmart.com.tw/SalePage/Index/2448515'}, 
# {'Category': 'daily_use', 'Date': '2022-08-25', 'Market': 'pxgo',  'Price': '516', 
# 'Product_name': '【分批取】舒潔濕式衛生紙(40抽x3包)', 'Url': 'https://shop.pxmart.com.tw/SalePage/Index/2299297'}, 
# {'Category': 'daily_use', 'Date': '2022-08-25', 'Market': 'pxgo',  'Price': '516', 
# 'Product_name': '【分批取】舒潔濕式衛生紙(40抽x3包)', 'Url': 'https://shop.pxmart.com.tw/SalePage/Index/2299297'}]



# data為爬蟲完成後return的JSON
# 欄位修改觸需補pic_url修改內容
def rtmart(data):
    collections = db['RT-Mart']
    collections.insert_many(data)
    date = datetime.date.today()
    collections.update_many({'date': f'{date}'}, {'$set':{'market': 'R'}}, upsert=False)


def carr(data):
    collections = db.Carrefour
    collections.insert_many(data)
    date = datetime.date.today()
    collections.update_many({'Date': f'{date}'}, {'$set':{'Market': 'C'}}, upsert=False)
    collections.update_many(
        {'Date': f'{date}'}, 
        {'$rename':{
            'Category': 'category', 
            'Date': 'date', 
            'Market': 'market', 
            'Price': 'price', 
            'Product_name': 'product_name', 
            'Url': 'product_url',
            'PicUrl': 'photos'}}, 
        upsert=False)


def pxmart(data):
    collections = db.PxMart
    collections.insert_many(data)
