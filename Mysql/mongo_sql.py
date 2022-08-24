import pymongo
from pymongo import MongoClient
from sql_model import Mart, Product, Category, Price, BASE
import sqlalchemy as sa
import pandas as pd

# mongodb cloud connection
client = MongoClient('mongodb+srv://admin:00065638@cluster0.fiqpaqd.mongodb.net/?retryWrites=true&w=majority')

mongo_db = client.test
collections = mongo_db.pxmart_product
result = collections.find({}, {'_id': 0})
result_list = []

for i in result:
    result_list.append(i)
print(result_list)
for k, v in result_list[0].items():
    print(k, v)



# data1 = Product(product_name=result_list[4], category_id=8, mart_id="P")
# data2 = Price(date=, price=result_list[4]['price'], product_id=data1.id)






# # 使用sa.create_engine設定數據庫的連接信息
# engine = sa.create_engine('mysql+pymysql://root:00065638@localhost:3306/demo1', echo=True)
# # 定義session 可以去連接數據庫 用來插入數據, 查詢數據
# Session = sa.orm.sessionmaker(bind=engine)
# # 通過調用Base裡面的metadata.create_all()方法把engine傳入去建立數據庫
# # 會把BASE CLASS的子類(現在是user) 建立到數據庫裡面
# BASE.metadata.create_all(engine)
#
# data1 = Product(product_name=result_list[4], category_id=8, mart_id="P")
#
#
# # 建立一個session
# session = Session()
# # 有了session後 就可以調用session.add()去插入數據
# # 插入多筆數據
# session.add(data1)
# #
# # # 提交數據
# session.commit()
