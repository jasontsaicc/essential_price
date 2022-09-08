from flask import Flask, request, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import requests
import json
import configparser
import datetime
import cv2
import random
import string
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model, load_model
import os

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')
line_bot_api = LineBotApi(
    'CkapUp6WOUatCJpXulbIpWMcBZcQkKpz7cZIdwnX/e+yIYrSMhT9wJOZdTQ8nIUwFTyUZxROIqd/BGCWbSGxMeJpkltS9gjrX92GoZH/GNT7N+Sz0Z+pWiqr+DX9IVRw5UStv2YXEDtOQoaAbgJ/MwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('84fec8bfebea6ae5aaae6ad814fa244e')
end_point = config.get('line-bot', 'end_point')
HEADER = {
    'Content-type': 'application/json',
    'Authorization': f'Bearer {config.get("line-bot", "channel_access_token")}'
}


# setting MySQL
db = SQLAlchemy()
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://admin:tgi102aaa@projectdb.ckq7h3eivlb4.ap-northeast-1.rds.amazonaws.com:3306/essential"

db.init_app(app)


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return 'ok'
    body = request.json
    events = body["events"]
    # print(body)
    if "replyToken" in events[0]:
        payload = {}
        replyToken = events[0]["replyToken"]
        payload["replyToken"] = replyToken
        if events[0]["type"] == "message":
            if events[0]["message"]["type"] == "text":
                text = events[0]["message"]["text"]
                if text == "查詢歷史價格" or text == "查詢商品比價":
                    payload["messages"] = [confirmProduct(payload)]
                else:
                    payload["messages"] = [confirmSearch(text)]

            elif events[0]["message"]["type"] == "image":
                # 先儲存使用者傳入的照片
                pic_id = events[0]["message"]["id"]
                image_name = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(4))
                image_name = image_name + ".jpg"
                image_content = line_bot_api.get_message_content(pic_id)
                with open(f"./image/{image_name}", "wb") as i:
                    for pic in image_content.iter_content():
                        i.write(pic)
                payload["messages"] = [imgProcess(image_name)]

            replyMessage(payload)
        elif events[0]["type"] == "postback":
            data = json.loads(events[0]["postback"]["data"])
            if data['label'] == '查詢歷史價格':
                # 將data['text']傳入查詢歷史價格的SQL function, return result, tpye=list
                payload["messages"] = [
                    {
                        "type": "text",
                        "text": f"您欲查詢{data['text']}的歷史價格" +'\n' + connSQL(data)
                    }
                ]
            elif data['label'] == '查詢比價資訊':
                # 將data['text']傳入查詢比價的SQL function, return result, tpye=list
                payload["messages"] = [
                    {
                        "type": "text",
                        "text": f"您欲查詢{data['text']}的比價資訊"
                    }
                ]

            replyMessage(payload)

    return 'OK'



def connSQL(data):
    date = "2022-08-24"
    sql_cmd = f"""
        select
            product_name,
            price,
            product_url
        from product pd
            join price pr
                on pd.id = pr.product_id
        where
            pd.product_name like '%%{data["text"]}%%' and pr.date = '{date}'
        """
    query_data = db.engine.execute(sql_cmd)

    rows = list()
    
    for row in query_data:
        row = list(row)
        row[1] = "價格:" + str(row[1]) + "元"
        # row = str(row)
        # print(row)
        rows.append(row)

    rows = str(rows)
    useless = "\{'}]\"["

    for i in useless:
        rows = rows.replace(i,"")
    rows = rows.replace(",","\n")

    return rows



def confirmSearch(text):
    message = {
        "type": "template",
        "altText": "this is a confirm template",
        "template": {
            "type": "confirm",
            "text": "請選擇欲查詢項目",
            "actions": [
                {
                    "type": "postback",
                    "label": "查詢歷史價格",
                    "data": json.dumps({'text': text, 'label': "查詢歷史價格"})
                },
                {
                    "type": "postback",
                    "label": "查詢比價資訊",
                    "data": json.dumps({'text': text, 'label': "查詢比價資訊"})
                }
            ]
        }
    }
    return message


def confirmProduct(payload):
    payload["messages"] = [{"type": "text", "text": '請上傳商品圖片，或輸入商品名稱。'}]
    replyMessage(payload)


def historyPrice(events, payload):
    if events[0]["type"] == "message":
        if events[0]["message"]["type"] == "text":
            text = events[0]["message"]["text"]
            # result = {'type': 'text', 'text': f'您想查詢{text}的歷史價格'}
            result = connSQL(text)
        # elif
        return result


# def martPrice():
#     reply = '請上傳商品圖片，或輸入商品名稱。'
#     replyMessage(reply)
#     if events[0]["type"] == "message":
#         if events[0]["message"]["type"] == "text":
#             text = events[0]["message"]["text"]
#             result = f'您想查詢{text}的比價資訊'
#             # result = connSQL(text)
#         # elif
#         return result


def replyMessage(payload):
    r = requests.post("https://api.line.me/v2/bot/message/reply", data=json.dumps(payload), headers=HEADER)
    print(r.text)
    return 'OK'


def imgProcess(image_name):
    img_path = f"./image/{image_name}"
    img = cv2.imread(img_path)
    img = cv2.resize(img, (256, 256))
    img = np.array(img)
    img_array = []
    img_array.append(img)
    img_array = np.asarray(img_array)
    os.remove(img_path)
    return imgPredict(img_array)


def imgPredict(img):
    # 載入訓練好的model
    model_pred = tf.keras.models.load_model('G:/我的雲端硬碟/Colab_Notebooks/model_0830.h5')

    # Prediction
    pred = model_pred.predict(img)

    brand = {'iMeiMilk': 0, 'LimFengInMilk': 1, 'JuHsiangMilk': 2, 'FreshDelightMilk': 3, 'KuangChuanMilk': 4,
             'LargeReiSuiMilk': 5, 'SmallReiSuiMilk': 6, 'LowFatLargeReiSuiMilk': 7, 'LowFatSmallReiSuiMilk': 8}
    message = {"type": "text"}
    out = np.argmax(pred, axis=1)
    for i in brand:
        if out == brand[i]:
            message["text"] = i
    return message


# @app.route('/upload_file', methods=['POST'])
# def upload_file():
#     payload = dict()
#     if request.method == 'POST':
#         file = request.files['file']
#         print("json:", request.json)
# form = request.form
# age = form['age']
# gender = ("男" if form['gender'] == "M" else "女") + "性"
# if file:
#     filename = file.filename
#     img_path = os.path.join(UPLOAD_FOLDER, filename)
#     file.save(img_path)
#     print(img_path)
#     payload["to"] = my_line_id
#     payload["messages"] = [getImageMessage(F"{end_point}/{img_path}"),
#         {
#             "type": "text",
#             "text": F"年紀：{age}\n性別：{gender}"
#         }
#     ]
#     pushMessage(payload)
# return 'OK'


if __name__ == "__main__":
    app.run(debug=True)