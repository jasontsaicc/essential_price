import pymongo
from pymongo import MongoClient
import mysql.connector
from mysql.connector import errorcode

# mongodb cloud connection
client = MongoClient('mongodb+srv://admin:tgi102aaa@cluster0.19rsmeq.mongodb.net/?retryWrites=true&w=majority')

db = client.All_Market
collections = db.productions


# find from mongodb(不顯示id)
result = collections.find({}, {'_id':0})
result_list = []
for i in result:
    result_list.append(i)
    # print(type(i)) # 回傳結果是dic類型
    # print(i)
    for k, v in i.items():
      # print(k, v)
      # print(type(k), type(v))
      cursor.execute("INSERT INTO product (Category, Date, Market, Price, Product_name, Url) VALUES (%s, %s, %s, %s, %s, %s);", (v, v+1, v+2, int(v+3), v+4, v+5))
      print("Inserted",cursor.rowcount,"row(s) of data.")

print(result_list)
print()