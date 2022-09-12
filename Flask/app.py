from flask import Flask
from flask import send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from flask import request
from flask_paginate import Pagination, get_page_parameter

app = Flask(__name__)
db = SQLAlchemy()

# MySql datebase
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://admin:tgi102aaa@projectdb.ckq7h3eivlb4.ap-northeast-1.rds.amazonaws.com:3306/essential"

db.init_app(app)



# Read data


@app.route('/')
def hello_world():  # put application's code here
    prduct_sql = f"""SELECT product.id, product_name, product_pic_url, price from product JOIN price where product.id = price.product_id  order by rand() limit 8"""

    query_data = db.engine.execute(prduct_sql)
    query_data_list = []

    for i in query_data:
        query_data_list.append(i)



    Product1_id = query_data_list[0][0]
    name1 = query_data_list[0][1]
    pic_url1 = query_data_list[0][2]
    price1 = query_data_list[0][3]

    Product2_id = query_data_list[1][0]
    name2 = query_data_list[1][1]
    pic_url2 = query_data_list[1][2]
    price2 = query_data_list[1][3]

    Product3_id = query_data_list[2][0]
    name3 = query_data_list[2][1]
    pic_url3 = query_data_list[2][2]
    price3 = query_data_list[2][3]

    Product4_id = query_data_list[3][0]
    name4 = query_data_list[3][1]
    pic_url4 = query_data_list[3][2]
    price4 = query_data_list[3][3]

    Product5_id = query_data_list[4][0]
    name5 = query_data_list[4][1]
    pic_url5 = query_data_list[4][2]
    price5 = query_data_list[4][3]

    Product6_id = query_data_list[5][0]
    name6 = query_data_list[5][1]
    pic_url6 = query_data_list[5][2]
    price6 = query_data_list[5][3]

    Product7_id = query_data_list[6][0]
    name7 = query_data_list[6][1]
    pic_url7 = query_data_list[6][2]
    price7 = query_data_list[6][3]

    Product8_id = query_data_list[7][0]
    name8 = query_data_list[7][1]
    pic_url8 = query_data_list[7][2]
    price8 = query_data_list[7][3]

    print(query_data_list)


    return render_template('index-2.html', Product1_id=Product1_id,name1=name1,pic_url1=pic_url1, price1=price1, Product2_id=Product2_id,name2=name2,pic_url2=pic_url2, price2=price2, Product3_id=Product3_id,name3=name3,pic_url3=pic_url3, price3=price3, Product4_id=Product4_id,name4=name4,pic_url4=pic_url4, price4=price4, Product5_id=Product5_id,name5=name5,pic_url5=pic_url5, price5=price5, Product6_id=Product6_id,name6=name6,pic_url6=pic_url6, price6=price6, Product7_id=Product7_id,name7=name7,pic_url7=pic_url7, price7=price7, Product8_id=Product8_id,name8=name8,pic_url8=pic_url8, price8=price8)


@app.route('/index')
def index():  # put application's code here
    return render_template('index-2.html')



@app.route('/shop/<Category_id>')
def category(Category_id):  # put application's code here
    search = False
    q = request.args.get('page', 1)
    int_page = int(q)

    end = (int_page - 1) * 12
    print(int_page)
    # if q:
    #     search = True

    page = request.args.get(get_page_parameter(), type=int, default=1)

    count_category_sql = f""" SELECT distinct count(*) from product JOIN price where product.id = price.product_id and category_id = "{Category_id}" """
    count_category_query_data = db.engine.execute(count_category_sql)
    query_data_list = []

    for i in count_category_query_data:
        query_data_list.append(i)
    count_category_data = query_data_list[0][0]
    pagination = Pagination(page=page, per_page=12, total=count_category_data, search=search)

    category_sql = f""" SELECT distinct product.id, product_name, product_pic_url, price from product JOIN price where product.id = price.product_id and category_id = "{Category_id}" limit 12 offset {end} """
    query_data = db.engine.execute(category_sql)
    query_data_list = []

    for i in query_data:
        query_data_list.append(i)
    print(query_data_list)

    product_id1 = query_data_list[0][0]
    name1 = query_data_list[0][1]
    pic_url1 = query_data_list[0][2]
    price1 = query_data_list[0][3]

    product_id2 = query_data_list[1][0]
    name2 = query_data_list[1][1]
    pic_url2 = query_data_list[1][2]
    price2 = query_data_list[1][3]

    product_id3 = query_data_list[2][0]
    name3 = query_data_list[2][1]
    pic_url3 = query_data_list[2][2]
    price3 = query_data_list[2][3]

    product_id4 = query_data_list[3][0]
    name4 = query_data_list[3][1]
    pic_url4 = query_data_list[3][2]
    price4 = query_data_list[3][3]

    product_id5 = query_data_list[4][0]
    name5 = query_data_list[4][1]
    pic_url5 = query_data_list[4][2]
    price5 = query_data_list[4][3]

    product_id6 = query_data_list[5][0]
    name6 = query_data_list[5][1]
    pic_url6 = query_data_list[5][2]
    price6 = query_data_list[5][3]

    product_id7 = query_data_list[6][0]
    name7 = query_data_list[6][1]
    pic_url7 = query_data_list[6][2]
    price7 = query_data_list[6][3]

    product_id8 = query_data_list[7][0]
    name8 = query_data_list[7][1]
    pic_url8 = query_data_list[7][2]
    price8 = query_data_list[7][3]

    product_id9 = query_data_list[8][0]
    name9 = query_data_list[8][1]
    pic_url9 = query_data_list[8][2]
    price9 = query_data_list[8][3]

    product_id10 = query_data_list[9][0]
    name10 = query_data_list[9][1]
    pic_url10 = query_data_list[9][2]
    price10 = query_data_list[9][3]

    product_id11 = query_data_list[10][0]
    name11 = query_data_list[10][1]
    pic_url11 = query_data_list[10][2]
    price11 = query_data_list[10][3]

    product_id12 = query_data_list[11][0]
    name12 = query_data_list[11][1]
    pic_url12 = query_data_list[11][2]
    price12 = query_data_list[11][3]

    return render_template('shop.html', page=page, pagination=pagination,  Category_id=Category_id,  product_id1=product_id1, name1=name1, pic_url1=pic_url1, price1=price1, product_id2=product_id2, name2=name2, pic_url2=pic_url2, price2=price2, product_id3=product_id3, name3=name3, pic_url3=pic_url3, price3=price3, product_id4=product_id4, name4=name4, pic_url4=pic_url4, price4=price4, product_id5=product_id5, name5=name5, pic_url5=pic_url5, price5=price5, product_id6=product_id6, name6=name6, pic_url6=pic_url6, price6=price6, product_id7=product_id7, name7=name7, pic_url7=pic_url7, price7=price7, product_id8=product_id8, name8=name8, pic_url8=pic_url8, price8=price8, product_id9=product_id9, name9=name9, pic_url9=pic_url9, price9=price9, product_id10=product_id10, name10=name10, pic_url10=pic_url10, price10=price10, product_id11=product_id11, name11=name11, pic_url11=pic_url11, price11=price11, product_id12=product_id12, name12=name12, pic_url12=pic_url12, price12=price12)


@app.route('/shop-details/<Product_id>')
def shop_details(Product_id):  # put application's code here
    prduct_sql = f"""SELECT product.id, product_name, product_pic_url, price, category_id, date, product_url from product JOIN price where product.id = price.product_id and product.id = {Product_id}"""
    query_data = db.engine.execute(prduct_sql)
    query_data_list = []

    for i in query_data:
        query_data_list.append(i)

    print(query_data_list)
    Product_id = query_data_list[0][0]
    name = query_data_list[0][1]
    pic_url = query_data_list[0][2]
    price = query_data_list[0][3]
    category_id = query_data_list[0][4]
    date = query_data_list[0][5]
    product_url = query_data_list[0][6]
    return render_template('shop-details.html', Product_id=Product_id, name=name, pic_url=pic_url, price=price, category_id=category_id, date=date, product_url=product_url)


if __name__ == '__main__':
    app.run()
