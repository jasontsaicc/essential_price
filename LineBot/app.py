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
import re
import jieba

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')
line_bot_api = LineBotApi('Channel access token')
handler = WebhookHandler('Channel secret')
end_point = config.get('line-bot', 'end_point')
HEADER = {
    'Content-type': 'application/json',
    'Authorization': f'Bearer {config.get("line-bot", "channel_access_token")}'
}

# setting MySQL
db = SQLAlchemy()
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "SQLALCHEMY_DATABASE_URI"

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
                payload["messages"] = [imgPredict(image_name)]

            replyMessage(payload)
        elif events[0]["type"] == "postback":
            data = json.loads(events[0]["postback"]["data"])
            if data['label'] == '查詢歷史價格':
                # 將data['text']傳入查詢歷史價格的SQL function
                price = historySQL(data['text'])
                result = resultSQL(price)
                payload["messages"] = [
                        {
                            "type": "text",
                            "text": f"{data['text']}的歷史價格如下：" + "\n" + result
                        }
                    ]
            elif data['label'] == '查詢比價資訊':
                # 將data['text']傳入查詢比價的SQL function
                price = priceSQL(data['text'])
                result = resultSQL(price)
                payload["messages"] = [
                        {
                            "type": "text",
                            "text": f"{data['text']}的比價資訊如下：" + "\n" + result
                        }
                    ]
            
            replyMessage(payload)
        else:
            payload["messages"] = [
                        {
                            "type": "text",
                            "text": "無法識別您輸入的內容，請依規定格式重新輸入。"
                        }
                    ]
    return 'OK'


def priceSQL(text):
    date = "2022-08-29"
    sql_cmd = f"""
        select
            pd.product_name,
            pd.mart_id,
            pr.price,
            pd.product_url
        from product pd
            join price pr
                on pd.id = pr.product_id
        where
            pd.product_name regexp '[{text}]' and pr.`date` = '{date}'
        """
    query_data = db.engine.execute(sql_cmd)

    rows = []
    
    for row in query_data:
        row = list(row)
        row[2] = "價格:" + f"{row[2]}" + "元"
        rows.append(row)

    return jieba_cut(rows, text)


def historySQL(text):
    sql_cmd = f"""
        select
            pd.product_name,
            pd.mart_id,
            pr.product_id
        from product pd
            join price pr
                on pd.id = pr.product_id
        where
            pd.product_name regexp '[{text}]'  and pr.`date` = '2022-08-24'
        """
    query_data = db.engine.execute(sql_cmd)

    rows = []
    
    for row in query_data:
        row = list(row)
        p_id = row.pop(2)
        row.append("網址" + f"{p_id}")  # 待更新網址
        rows.append(row)
    
    return jieba_cut(rows, text)


def resultSQL(price):
    price_p = []
    price_r = []
    price_c = []
    for i in price:
        if i[1] == 'P':
            del i[1]
            if "全聯" not in price_p:
                price_p.append("全聯")
            price_p.append(str(i))
        elif i[1] == 'C':
            del i[1]
            if "家樂福" not in price_c:
                price_c.append("家樂福")
            price_c.append(str(i))
        elif i[1] == 'R':
            del i[1]
            if "大潤發" not in price_r:
                price_r.append("大潤發")
            price_r.append(str(i))
    price = [price_p, price_c, price_r]
    for i in price:
        i = str(i)
    price = str(price)
    useless = "\\{'}]\"[\'"
    for i in useless:
        price = price.replace(i, "")
    price = price.replace(",", "\n")
    return price


def jieba_cut(rows, text):
    letter = list(jieba.cut(text, cut_all=False, HMM=True))
    return_list = []
    for j in rows:
        percent = len(letter) * 0.4
        n = 0
        for i in letter:
            pattern0 = re.compile((letter[0]))
            compare0 = pattern0.search(j[0])
            if compare0 is None:
                break
            else:
                pattern = re.compile((i))
                compare = pattern.search(j[0])
                if compare is not None:
                    if n >= percent and j not in return_list:
                        return_list.append(j)
                    n += 1
    return return_list


def confirmSearch(text):
    pattern = r"[^$!?！？^#|,@&=\+\.]"
    var = re.compile(pattern)
    result = var.search(text)
    if result is not None:
        message = {
                    "type": "template",
                    "altText": "this is a confirm template",
                    "template": {
                        "type": "confirm",
                        "text": f"查詢品項為{text}，請選擇欲查詢項目。",
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
    else:
        message = {"type": "text", "text": "輸入內容請勿包含特殊字元，請重新輸入。"}
    
    return message


def replyMessage(payload):
    r = requests.post("https://api.line.me/v2/bot/message/reply", data=json.dumps(payload), headers=HEADER)
    return 'OK'


def imgProcess(image_name):
    # 將使用者傳入的圖片處理成模型可辨識格式
    img_path = f"./image/{image_name}"
    img = cv2.imread(img_path)
    img = cv2.resize(img, (256, 256))
    img = np.array(img)
    img_array = []
    img_array.append(img)
    img_array = np.asarray(img_array)
    os.remove(img_path)
    return img_array


def imgPredict(img_name):
    # 先處理圖片
    img = imgProcess(img_name)
    
    # 載入訓練好的model
    model_pred = tf.keras.models.load_model('G:/我的雲端硬碟/Colab_Notebooks/model_0830.h5') # 部屬前須更新
  
    # Prediction
    pred = model_pred.predict(img)

    brand = {0: '義美全脂鮮乳', 1: '林鳳營全脂鮮乳', 2: '乳香世家鮮乳', 3: '福樂一番鮮特極鮮乳', 4: '光泉鮮乳', 
            5: '瑞穗全脂鮮奶', 6: '瑞穗全脂鮮奶', 7: '瑞穗低脂鮮奶', 8: '瑞穗低脂鮮奶'}
    out = np.argmax(pred, axis=1)
    for i in brand:
        if out == brand[i]:
            pd_name = i
            return confirmSearch(pd_name)


if __name__ == "__main__":
    app.run()
