
import sqlalchemy as sa
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

BASE = declarative_base()


class Mart(BASE):
    __tablename__ = 'marts'
    id = sa.Column(sa.String(64), primary_key=True)
    mart_name = sa.Column(sa.String(255), unique=True)

    fk_product_mart = relationship('Product')


class Product(BASE):
    __tablename__ = 'product'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    # mart_id = sa.Column(sa.String(64))
    # category_id = sa.Column(sa.Integer)
    product_name = sa.Column(sa.String(64))

    fk_price = relationship('Price')

    category_id = sa.Column(sa.Integer, sa.ForeignKey('category.id'))
    mart_id = sa.Column(sa.String(64), sa.ForeignKey('marts.id'))


class Category(BASE):
    __tablename__ = 'category'
    id = sa.Column(sa.Integer, primary_key=True)
    category_name = sa.Column(sa.String(64), unique=True, )

    fk_product_category = relationship('Product')


class Price(BASE):
    __tablename__ = 'price'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    # product_id = sa.Column(sa.Integer)
    date = sa.Column(sa.Date)
    price = sa.Column(sa.Integer)

    product_id = sa.Column(sa.Integer, sa.ForeignKey('product.id'))


# 使用sa.create_engine設定數據庫的連接信息
engine = sa.create_engine('mysql+pymysql://root:00065638@localhost:3306/demo1', echo=True)
# 定義session 可以去連接數據庫 用來插入數據, 查詢數據
Session = sa.orm.sessionmaker(bind=engine)
# 通過調用Base裡面的metadata.create_all()方法把engine傳入去建立數據庫
# 會把BASE CLASS的子類(現在是user) 建立到數據庫裡面
BASE.metadata.create_all(engine)

# insert 數據

# # Marts
# px_marts = Mart(id="P", mart_name="全聯")
# # rt_mart = Mart(id='R', mart_name='大潤發')
# # carrefour_mart = Mart(id='C', mart_name='家樂福')
# # poya_mart = Mart(id='Y', mart_name='寶雅')
#
# # all_marts = [px_mart, rt_mart, carrefour_mart, poya_mart]
#
#
# # 建立一個session
# session = Session()
# # 有了session後 就可以調用session.add()去插入數據
#
# #
# # # 插入多筆數據
# session.add(px_marts)
# #
# # # 提交數據
# session.commit()
