from tgi102_flask.app.elasticsearch_qurey.elasticsearch_query_class import elasticsearch
from tgi102_flask import app, db, render_template, request, get_page_parameter, Pagination, session, redirect, url_for
from tgi102_flask.model import Product, Price, Category, Mart
from tgi102_flask.app.ai_model.md_test import milk_model


@app.route('/index')
@app.route('/')
def index():

    index_sql = db.session.query(Product, Price).filter(Product.id == Price.product_id).order_by(db.func.rand()).limit(8)
    query_data_list = []
    for i in index_sql:
        query_data_list.append(i)

    print("query_data_list", query_data_list)
    return render_template('index-2.html', query_data_list=query_data_list)


@app.route('/shop/<Category_id>')
def category(Category_id):  # put application's code here
    search = False
    q = request.args.get('page', 1)
    int_page = int(q)
    end = (int_page - 1) * 12
    # if q:
    #     search = True

    page = request.args.get(get_page_parameter(), type=int, default=1)

    count_category_sql = db.session.query(db.func.count(Product.id)).filter(Product.id == Price.product_id).filter(Product.category_id == Category_id).all()[0][0]
    print(count_category_sql)

    pagination = Pagination(page=page, per_page=12, total=count_category_sql, search=search)

    category_sql = db.session.query(Product, Price).filter(Product.id == Price.product_id).filter(Product.category_id == Category_id).order_by(db.func.rand()).limit(12).offset(end)
    query_data_list = []

    for i in category_sql:
        query_data_list.append(i)
    print("query_data_list",  query_data_list)

    return render_template('shop.html', page=page, pagination=pagination,  Category_id=Category_id, query_data_list=query_data_list)


@app.route('/shop-details/<product_id_query>')
def shop_details(product_id_query):  # put application's code here
    print("product_id_query", product_id_query)
    details_product_sql = db.session.query(Product, Price).filter(Product.id == Price.product_id).filter(Product.id == {product_id_query}).first()
    print("details_product_sql", details_product_sql)
    query_data_list = []
    for i in details_product_sql:
        query_data_list.append(i)
    print("query_data_list", query_data_list)

    details_Product_id = query_data_list[0].id
    details_name = query_data_list[0].product_name
    details_pic_url = query_data_list[0].product_pic_url
    details_price = query_data_list[1].price
    details_category_id = query_data_list[0].category_id
    details_date = query_data_list[1].date
    details_product_url = query_data_list[0].product_url
    print("query_data_list[0]", query_data_list[0])
    print("query_data_list[1]", query_data_list[1])

    return render_template('shop-details.html', details_Product_id=details_Product_id, details_name=details_name, details_pic_url=details_pic_url, details_price=details_price, details_category_id=details_category_id, details_date=details_date, details_product_url=details_product_url)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error)


# @app.route('/update-pic', methods=["GET", "POST"])
# def uploadprocess():
#     print('upload post')
#     if 'input-id' not in request.files:
#         return jsonify({"errno": 100, "errmsg": "無檔案"})
#     if request.method == 'POST':
#         files = request.files.getlist('input-id')
#
#         for file in files:
#             filename = file.filename
#             print("file", file)
#             print("filename", filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             print(jsonify({"errno": 0, "errmsg": "上傳成功"}))
#
#         return jsonify({"errno": 0, "errmsg": "上傳成"})
#     return render_template('blog-details.html')

@app.route('/upload_search', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        files = request.files.getlist('file')
        photo = request.files['file'].read()
        # print("photo", photo)

        for file in files:
            filename = file.filename
            print("filename", filename)
            # file.save(app.config['UPLOAD_FOLDER'], filename)
            file.save(f'tgi102_flask/static/upload/{filename}')
        upload_photo = f'/static/upload/{filename}'
        print("upload_photo", upload_photo)

        # img = cv2.imread(f'tgi102_flask/static/upload/{filename}')
        # print("img", img)

        photo_fromstring = np.fromstring(photo, np.uint8)
        print("photo_fromstring", photo_fromstring)
        photo_imdecode = cv2.imdecode(photo_fromstring, cv2.IMREAD_COLOR)[:, :, ::-1]
        # milk_model(photo_imdecode)
        result = milk_model(photo_imdecode)


        return redirect(url_for('uploaded_file', filename=result))
    return render_template('upload_search.html')


@app.route('/search_photo/<filename>')
def uploaded_file(filename):
    return render_template('result_2.html', filename=filename)


@app.route('/search', methods=['get', 'POST'])
def search():
    if request.method == 'POST':
        # 取出keyword
        keyword = request.form['keyword']
        print("keyword", keyword)
        return redirect(url_for("search_results", query=keyword))
    else:
        return render_template('index-2.html')


@app.route('/search_results/<query>')
def search_results(query):
    es = elasticsearch(index_name="essential", index_type='_doc')
    data = es.search(query)

    address_data = data['hits']['hits']
    total = data['hits']['total']['value']
    address_list = []
    print("data", data)
    print("total", total)

    for item in address_data:
        address_list.append(item['_source'])

    search = False
    q = request.args.get('page', 1)
    int_page = int(q)
    end = (int_page - 1) * 12
    # if q:
    #     search = True

    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, per_page=12, total=total, search=search)

    # new_data = json.dumps(address_list)
    # # print("new_data", new_data)
    # return app.response_class(new_data, content_type='application/json')

    return render_template('search_results.html', page=page, pagination=pagination, query=query, return_list=address_list)


if __name__ == '__main__':
    app.run(debug=True)
