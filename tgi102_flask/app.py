import os
import numpy as np
import cv2
import tensorflow as tf

from tgi102_flask import app, render_template, request, get_page_parameter, Pagination, redirect, url_for
from tgi102_flask.model import get_index_data, get_count_category, get_category_product, get_shop_details
from tgi102_flask.app.elasticsearch_qurey.elasticsearch_query_class import elasticsearch


@app.route('/index')
@app.route('/')
def index():
    index_data = get_index_data()
    print("query_data_list", index_data)

    return render_template('index-2.html', query_data_list=index_data)


@app.route('/shop/<category_id>')
def category(category_id):
    # get page parameter
    pagination_search = False
    q = request.args.get('page', 1)
    int_page = int(q)
    end = (int_page - 1) * 12
    # if q:
    #     search = True

    page = request.args.get(get_page_parameter(), type=int, default=1)
    count_category = get_count_category(category_id)
    pagination = Pagination(page=page, per_page=12, total=count_category, search=pagination_search)

    category_product_data = get_category_product(category_id, end)

    return render_template('shop.html', page=page, pagination=pagination, Category_id=category_id,
                           query_data_list=category_product_data)


@app.route('/shop-details/<product_id_query>')
def shop_details(product_id_query):
    shop_details_data = get_shop_details(product_id_query)

    return render_template('shop-details.html', query_data_list=shop_details_data)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error)


@app.route('/upload_search', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        files = request.files.getlist('file')
        photo = request.files['file'].read()
        # print("photo", photo)

        for file in files:
            filename = file.filename
            print("filename", filename)
            # 判斷資料夾是否存在
            path = 'tgi102_flask/static/upload'
            if not os.path.isdir(path):
                os.mkdir(path)
            # file.save(app.config['UPLOAD_FOLDER'], filename)
            file.save(f'tgi102_flask/static/upload/{filename}')
        upload_photo = f'/static/upload/{filename}'
        print("upload_photo", upload_photo)

        # img = cv2.imread(f'tgi102_flask/static/upload/{filename}')
        # print("img", img)

        photo_fromstring = np.fromstring(photo, np.uint8)
        print("photo_fromstring", photo_fromstring)
        photo_imdecode = cv2.imdecode(photo_fromstring, cv2.IMREAD_COLOR)[:, :, ::-1]
        # result = milk_model(photo_imdecode)

        img_resize = cv2.resize(photo_imdecode, (224, 224))
        img_astype = img_resize.astype(np.float32)
        img_array = []
        img_array.append(img_astype)
        img_asarray = np.asarray(img_array)
        result = predict(img_array)
        print(result)

        return redirect(url_for('search_results', query=result))
    return render_template('upload_search.html')


@app.route('/search_photo/<filename>')
def uploaded_file(filename):
    return render_template('result_2.html', filename=filename)


def predict(img_array):
    img = img_array
    model_pred = tf.lite.Interpreter('./tflite_model.tflite')
    model_pred.allocate_tensors()
    input_index = model_pred.get_input_details()[0]["index"]
    output_index = model_pred.get_output_details()[0]["index"]

    model_pred.set_tensor(input_index, img)
    model_pred.invoke()

    output_data = model_pred.get_tensor(output_index)
    print(output_data)
    x = np.argmax(output_data)

    brand = {0: '義美全脂鮮乳', 1: '林鳳營全脂鮮乳', 2: '乳香世家鮮乳', 3: '福樂一番鮮特極鮮乳', 4: '光泉鮮乳',
             5: '瑞穗全脂鮮奶', 6: '瑞穗全脂鮮奶', 7: '瑞穗低脂鮮奶', 8: '瑞穗低脂鮮奶'}

    if np.max(output_data) > 0.7:
        for i in brand:
            if i == x:
                pd_name = brand[i]
                print("Prediction:", pd_name)
        return pd_name
    else:
        return "無法辨識"


@app.route('/search', methods=['get', 'POST'])
def search():
    if request.method == 'POST':
        # get search keyword
        keyword = request.form['keyword']
        print("keyword", keyword)
        return redirect(url_for("search_results", query=keyword))
    else:
        return render_template('index-2.html')


@app.route('/search_results/<query>')
def search_results(query, result_name=None):
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
    # if q:ls
    #     search = True

    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, per_page=12, total=total, search=search)

    return render_template('search_results.html', page=page, pagination=pagination, query=query,
                           return_list=address_list, result_name=result_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
