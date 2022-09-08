from flask import Flask
from flask import send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from flask import request

app = Flask(__name__)
db = SQLAlchemy()

# MySql datebase
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://admin:tgi102aaa@projectdb.ckq7h3eivlb4.ap-northeast-1.rds.amazonaws.com:3306/essential"

db.init_app(app)



# Read data


@app.route('/')
def hello_world():  # put application's code here


    return render_template('index-2.html')


@app.route('/index')
def index():  # put application's code here
    return render_template('index-2.html')


@app.route('/shop')
def shop():  # put application's code here
    return render_template('shop.html')



@app.route('/shop-details/<Product_id>')
def shop_details(Product_id):  # put application's code here

    prduct_sql = f"""SELECT product.id, product_name, product_pic_url, price from product JOIN price where product.id = price.product_id and product.id = {Product_id}"""

    query_data = db.engine.execute(prduct_sql)
    query_data_list = []

    for i in query_data:
        query_data_list.append(i)

    print(query_data_list)
    Product_id = query_data_list[0][0]
    name = query_data_list[0][1]
    pic_url = query_data_list[0][2]
    price = query_data_list[0][3]
    return render_template('shop-details.html', Product_id=Product_id, name=name, pic_url=pic_url, price=price)


if __name__ == '__main__':
    app.run()
