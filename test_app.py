from flask import Flask, request, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import requests
import json
import configparser
import datetime

app = Flask(__name__)
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
my_line_id = config.get('line-bot', 'my_line_id')
end_point = config.get('line-bot', 'end_point')
line_login_id = config.get('line-bot', 'line_login_id')
line_login_secret = config.get('line-bot', 'line_login_secret')
my_phone = config.get('line-bot', 'my_phone')
HEADER = {
    'Content-type': 'application/json',
    'Authorization': f'Bearer {config.get("line-bot", "channel_access_token")}'
}

# setting MySQL
db = SQLAlchemy()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://admin:tgi102aaa@projectdb.ckq7h3eivlb4.ap-northeast-1.rds.amazonaws.com/essential"

db.init_app(app)


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return 'ok'
    body = request.json
    events = body["events"]
    print(body)
    if "replyToken" in events[0]:
        payload = dict()
        replyToken = events[0]["replyToken"]
        payload["replyToken"] = replyToken
        if events[0]["type"] == "message":
            if events[0]["message"]["type"] == "text":
                text = events[0]["message"]["text"]

                if text == "查詢歷史價格":
                    payload["messages"] = [ProductConfirm()]
                    text == ""
                elif text == "查詢商品比價":
                    payload["messages"] = [getPlayStickerMessage()]
                else:
                    payload["messages"] = [ProductConfirm()]
               
                replyMessage(payload)
            elif events[0]["message"]["type"] == "location":
                title = events[0]["message"]["title"]
                latitude = events[0]["message"]["latitude"]
                longitude = events[0]["message"]["longitude"]
                payload["messages"] = [getLocationConfirmMessage(title, latitude, longitude)]
                replyMessage(payload)

    return 'OK'


@app.route('/dbMart')
def martSQL(data):
    date = datetime.date.today()
    sql_cmd = f"""
        select 
            pd.product_name, 
            pr.price
        from product pd
            join price pr
                on pd.id = pr.product_id
        where 
            pd.product_name like '%{data["title"]}%' and pr.`date` = {date}
        """

    query_data = db.engine.execute(sql_cmd)
    print(query_data)
    return 'ok'


@app.route('/dbHistory')
def historySQL(data):
    sql_cmd = f"""
        select 
            pd.product_name, 
            pr.price
        from product pd
            join price pr
                on pd.id = pr.product_id
        where pd.product_name like f'%{data["title"]}%'
        """

    query_data = db.engine.execute(sql_cmd)
    print(query_data)
    return 'ok'


def getMartPrice(data):
    message = {
                "type": "template",
                "altText": "this is a image carousel template",
                "template": {
                    "type": "image_carousel",
                    "columns": [
                    {
                        "imageUrl": f"{end_point}/static/taipei_101.jpeg",
                        "action": {
                        "type": "postback",
                        "label": "台北101",
                        "data": json.dumps(data)
                        }
                    },
                    {
                        "imageUrl": f"{end_point}/static/taipei_1.jpeg",
                        "action": {
                        "type": "postback",
                        "label": "台北101",
                        "data": json.dumps(data)
                        }
                    }
                    ]
                }
            }
    return message


def ProductConfirm(payload):
    data = {"title": title}
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
                        "data": json.dumps(data)
                    },
                    {
                        "type": "postback",
                        "label": "查詢比價結果",
                        "data": json.dumps(data)
                    }
                    ]
                }
            }
    return message



@app.route('/upload_file', methods=['POST'])
def upload_file():
    payload = dict()
    if request.method == 'POST':
        file = request.files['file']
        print("json:", request.json)
        form = request.form
        age = form['age']
        gender = ("男" if form['gender'] == "M" else "女") + "性"
        if file:
            filename = file.filename
            img_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(img_path)
            print(img_path)
            payload["to"] = my_line_id
            payload["messages"] = [getImageMessage(F"{end_point}/{img_path}"),
                {
                    "type": "text",
                    "text": F"年紀：{age}\n性別：{gender}"
                }
            ]
            pushMessage(payload)
    return 'OK'