from sql_model import Mart, Product, Category, Price, BASE
import sqlalchemy as sa


# 使用sa.create_engine設定數據庫的連接信息
engine = sa.create_engine('mysql+pymysql://root:00065638@localhost:3306/demo1', echo=True)
# 定義session 可以去連接數據庫 用來插入數據, 查詢數據
Session = sa.orm.sessionmaker(bind=engine)
# 通過調用Base裡面的metadata.create_all()方法把engine傳入去建立數據庫
# 會把BASE CLASS的子類(現在是user) 建立到數據庫裡面
BASE.metadata.create_all(engine)

# add Marts
px_marts = Mart(id="P", mart_name="全聯")
rt_mart = Mart(id='R', mart_name='大潤發')
carrefour_mart = Mart(id='C', mart_name='家樂福')
poya_mart = Mart(id='Y', mart_name='寶雅')

"""生鮮食品：fresh_food
冷凍食品：frozen_food
飲料零食：drink_snacks
米油沖泡：rice_oil_powder
美妝護理：make_up
母嬰保健：baby
生活休閒：life_style
日用百貨：daily_use
家具寢飾：furniture
服飾鞋包：clothing
大小家電：electrical_3C
"""
# add Category
fresh_food = Category(id=1, category_name='fresh_food')
frozen_food = Category(id=2, category_name='frozen_food')
drink_snacks = Category(id=3, category_name='drink_snacks')
rice_oil_powder = Category(id=4, category_name='rice_oil_powder')
make_up = Category(id=5, category_name='make_up')
baby = Category(id=6, category_name='baby')
life_style = Category(id=7, category_name='life_style')
daily_use = Category(id=8, category_name='daily_use')
furniture = Category(id=9, category_name='furniture')
clothing = Category(id=10, category_name='clothing')
electrical_3C = Category(id=11, category_name='electrical_3C')

# 建立一個session
session = Session()
# 有了session後 就可以調用session.add()去插入數據

#
# # 插入多筆數據
session.add_all([px_marts, rt_mart, carrefour_mart, poya_mart,  fresh_food, frozen_food, drink_snacks, rice_oil_powder, make_up, baby, life_style, daily_use, furniture, clothing, electrical_3C])
#
# # 提交數據
session.commit()
