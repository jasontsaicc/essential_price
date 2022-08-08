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

# all_marts = [px_marts, rt_mart, carrefour_mart, poya_mart]


# 建立一個session
session = Session()
# 有了session後 就可以調用session.add()去插入數據

#
# # 插入多筆數據
session.add_all([px_marts, rt_mart, carrefour_mart, poya_mart])
#
# # 提交數據
session.commit()
