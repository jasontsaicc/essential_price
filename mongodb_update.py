import pymongo
from pymongo import MongoClient
import datetime

client = MongoClient('mongodb+srv://admin:<password>@cluster0.19rsmeq.mongodb.net/?retryWrites=true&w=majority')

db = client.All_Market
collections = db.productions

# update
update_data = collections.update_many({}, {'$set':{'Market': 'P'}}, upsert=False)
result = collections.find({'Date': f'{date}'}, {'_id':0})

for i in result:
    # print(type(i)) # 回傳結果是dic類型
    print(i)