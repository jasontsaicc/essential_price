
import sqlalchemy as sa
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()


class Mart(BASE):
    __tablename__ = 'marts'
    mart_id = sa.Column(sa.String(64), primary_key=True)
    mart_name = sa.Column(sa.String(255), unique=True)


class Product(BASE):
    __tablename__ = 'product'
    product_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    mart_id = sa.Column(sa.String(64))
    category_id = sa.Column(sa.Integer)
    product_name = sa.Column(sa.String(64), unique=True)


class Category(BASE):
    __tablename__ = 'category'
    category_id = sa.Column(sa.String(64), primary_key=True)
    category_name = sa.Column(sa.String(64), unique=True)


class Price(BASE):
    __tablename__ = 'Price'
    price_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    Product_ID = sa.Column(sa.Integer)
    date = sa.Column(sa.Date)
    price = sa.Column(sa.Integer)


# 使用sa.create_engine設定數據庫的連接信息
engine = sa.create_engine('mysql+pymysql://root:00065638@localhost:3306/demo')
# 定義session 可以去連接數據庫 用來插入數據, 查詢數據
Session = sa.orm.sessionmaker(bind=engine)
# 通過調用Base裡面的metadata.create_all()方法把engine傳入去建立數據庫
# 會把BASE CLASS的子類(現在是user) 建立到數據庫裡面
BASE.metadata.create_all(engine)

# insert 數據

# Category
px_mart = Category(category_id='P', category_name='全聯')
RT_mart = Category(category_id='R', category_name='大潤發')
carr_mart = Category(category_id='C', category_name='家樂福')
BO_mart = Category(category_id='Y', category_name='寶雅')




# 建立一個session
session = Session()
# 有了session後 就可以調用session.add()去插入數據
#
#
# 插入多筆數據
session.add_all([px_mart])
#
# 提交數據
session.commit()
#
