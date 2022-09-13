from tgi102_flask import app, db, render_template, request, get_page_parameter, Pagination, session
from tgi102_flask.models import product, price, category, mart

@app.route('/')
def hello_world():  # put application's code here
    index_sql = db.session.query(product.Product, price.Price).filter(product.Product.id == price.Price.product_id).order_by(db.func.rand()).limit(8)
    query_data_list = []

    for i in index_sql:
        query_data_list.append(i)

    Product1_id = query_data_list[0][0].id
    name1 = query_data_list[0][0].product_name
    pic_url1 = query_data_list[0][0].product_pic_url
    price1 = query_data_list[0][1].price

    Product2_id = query_data_list[1][0].id
    name2 = query_data_list[1][0].product_name
    pic_url2 = query_data_list[1][0].product_pic_url
    price2 = query_data_list[1][1].price

    Product3_id = query_data_list[2][0].id
    name3 = query_data_list[2][0].product_name
    pic_url3 = query_data_list[2][0].product_pic_url
    price3 = query_data_list[2][1].price

    Product4_id = query_data_list[3][0].id
    name4 = query_data_list[3][0].product_name
    pic_url4 = query_data_list[3][0].product_pic_url
    price4 = query_data_list[3][1].price

    Product5_id = query_data_list[4][0].id
    name5 = query_data_list[4][0].product_name
    pic_url5 = query_data_list[4][0].product_pic_url
    price5 = query_data_list[4][1].price

    Product6_id = query_data_list[5][0].id
    name6 = query_data_list[5][0].product_name
    pic_url6 = query_data_list[5][0].product_pic_url
    price6 = query_data_list[5][1].price

    Product7_id = query_data_list[6][0].id
    name7 = query_data_list[6][0].product_name
    pic_url7 = query_data_list[6][0].product_pic_url
    price7 = query_data_list[6][1].price

    Product8_id = query_data_list[7][0].id
    name8 = query_data_list[7][0].product_name
    pic_url8 = query_data_list[7][0].product_pic_url
    price8 = query_data_list[7][1].price

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
    # if q:
    #     search = True

    page = request.args.get(get_page_parameter(), type=int, default=1)

    count_category_sql = db.session.query(db.func.count(product.Product.id)).filter(product.Product.id == price.Price.product_id).filter(product.Product.category_id == Category_id).all()[0][0]
    print(count_category_sql)

    pagination = Pagination(page=page, per_page=12, total=count_category_sql, search=search)

    category_sql = db.session.query(product.Product, price.Price).filter(product.Product.id == price.Price.product_id).filter(product.Product.category_id == Category_id).order_by(db.func.rand()).limit(12).offset(end)
    query_data_list = []

    for i in category_sql:
        query_data_list.append(i)
    print("query_data_list",  query_data_list)

    product_id1 = query_data_list[0][0].id
    name1 = query_data_list[0][0].product_name
    pic_url1 = query_data_list[0][0].product_pic_url
    price1 = query_data_list[0][1].price

    product_id2 = query_data_list[1][0].id
    name2 = query_data_list[1][0].product_name
    pic_url2 = query_data_list[1][0].product_pic_url
    price2 = query_data_list[1][1].price

    product_id3 = query_data_list[2][0].id
    name3 = query_data_list[2][0].product_name
    pic_url3 = query_data_list[2][0].product_pic_url
    price3 = query_data_list[2][1].price

    product_id4 = query_data_list[3][0].id
    name4 = query_data_list[3][0].product_name
    pic_url4 = query_data_list[3][0].product_pic_url
    price4 = query_data_list[3][1].price

    product_id5 = query_data_list[4][0].id
    name5 = query_data_list[4][0].product_name
    pic_url5 = query_data_list[4][0].product_pic_url
    price5 = query_data_list[4][1].price

    product_id6 = query_data_list[5][0].id
    name6 = query_data_list[5][0].product_name
    pic_url6 = query_data_list[5][0].product_pic_url
    price6 = query_data_list[5][1].price

    product_id7 = query_data_list[6][0].id
    name7 = query_data_list[6][0].product_name
    pic_url7 = query_data_list[6][0].product_pic_url
    price7 = query_data_list[6][1].price

    product_id8 = query_data_list[7][0].id
    name8 = query_data_list[7][0].product_name
    pic_url8 = query_data_list[7][0].product_pic_url
    price8 = query_data_list[7][1].price

    product_id9 = query_data_list[8][0].id
    name9 = query_data_list[8][0].product_name
    pic_url9 = query_data_list[8][0].product_pic_url
    price9 = query_data_list[8][1].price

    product_id10 = query_data_list[9][0].id
    name10 = query_data_list[9][0].product_name
    pic_url10 = query_data_list[9][0].product_pic_url
    price10 = query_data_list[9][1].price

    product_id11 = query_data_list[10][0].id
    name11 = query_data_list[10][0].product_name
    pic_url11 = query_data_list[10][0].product_pic_url
    price11 = query_data_list[10][1].price

    product_id12 = query_data_list[11][0].id
    name12 = query_data_list[11][0].product_name
    pic_url12 = query_data_list[11][0].product_pic_url
    price12 = query_data_list[11][1].price


    return render_template('shop.html', page=page, pagination=pagination,  Category_id=Category_id,  product_id1=product_id1, name1=name1, pic_url1=pic_url1, price1=price1, product_id2=product_id2, name2=name2, pic_url2=pic_url2, price2=price2, product_id3=product_id3, name3=name3, pic_url3=pic_url3, price3=price3, product_id4=product_id4, name4=name4, pic_url4=pic_url4, price4=price4, product_id5=product_id5, name5=name5, pic_url5=pic_url5, price5=price5, product_id6=product_id6, name6=name6, pic_url6=pic_url6, price6=price6, product_id7=product_id7, name7=name7, pic_url7=pic_url7, price7=price7, product_id8=product_id8, name8=name8, pic_url8=pic_url8, price8=price8, product_id9=product_id9, name9=name9, pic_url9=pic_url9, price9=price9, product_id10=product_id10, name10=name10, pic_url10=pic_url10, price10=price10, product_id11=product_id11, name11=name11, pic_url11=pic_url11, price11=price11, product_id12=product_id12, name12=name12, pic_url12=pic_url12, price12=price12)


@app.route('/shop-details/<Product_id>')
def shop_details(Product_id):  # put application's code here

    details_product_sql = db.session.query(product.Product, price.Price).filter(product.Product.id == {Product_id}).first()
    query_data_list = []

    for i in details_product_sql:
        query_data_list.append(i)

    details_Product_id = query_data_list[0].id
    details_name = query_data_list[0].product_name
    details_pic_url = query_data_list[0].product_pic_url
    details_price = query_data_list[1].price
    details_category_id = query_data_list[0].category_id
    details_date = query_data_list[1].date
    details_product_url = query_data_list[0].product_url
    return render_template('shop-details.html', details_Product_id=details_Product_id, details_name=details_name, details_pic_url=details_pic_url, details_price=details_price, details_category_id=details_category_id, details_date=details_date, details_product_url=details_product_url)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error)


if __name__ == '__main__':
    app.run(debug=True)
