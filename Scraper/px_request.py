from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime
import pymongo
from pymongo import MongoClient

import json
import time


# import pymongo


class Pxmart:
    # 初始化
    def __init__(self):
        self.url = None
        # 這裡可以設定要不要跑出瀏覽器出來 True 不顯示 False 顯示
        self.options = Options()
        self.options.headless = True
        # 不加載圖片,加快訪問速度
        self.options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        # 此步驟很重要，設置為開發者模式，防止被各大網站識別出來使用了Selenium
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 使用Chrome瀏覽器 後面會換成
        # self.driver = webdriver.Chrome("/Users/jasontsai/Desktop/tibame_subject/github/-essential_price/chromedriver")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

    # 使用del 讓程式結束的時候關閉瀏覽器
    def __del__(self):
        self.driver.close()

    def get_content(self, k, category_url):
        # 這裡傳入分類數字的list

            self.url = f'https://shop.pxmart.com.tw/v2/official/SalePageCategory/{category_url}'
            # 開啟網頁等待網頁載入完成
            self.driver.implicitly_wait(5)
            # 打開網址
            self.driver.get(self.url)
            time.sleep(2)
            try:
                res = []
                # 這裡設置3層for迴圈 一欄4個商品 跑25行會xpath前面的值會改變 所以外面再加個迴圈 這樣理論可以跑一個分類800樣商品
                for e in range(2, 10):
                    for i in range(1, 25):
                        js = "window.scrollTo(0,document.body.scrollHeight)"
                        self.driver.execute_script(js)
                        # time.sleep(0.2)
                        for j in range(1, 5):
                            category = self.driver.find_element('xpath',
                                                                f"//*[@id='root']/div/div[2]/div/ol/li[2]/a/h1")
                            name = self.driver.find_element('xpath',
                                                            f"//*[@id='root']/div/div[2]/div/div/div[2]/div[{e}]/div[1]/div/div[{i}]/div/div/ul/li[{j}]/div/div/a/div/div[2]/div[1]")
                            price = self.driver.find_element('xpath',
                                                             f"//*[@id='root']/div/div[2]/div/div/div[2]/div[{e}]/div[1]/div/div[{i}]/div/div/ul/li[{j}]/div/div/a/div/div[2]/div[2]/div[1]/div[2]")
                            # 這裡是用get_attribute 可以爬出屬性值
                            product_url = self.driver.find_element('xpath',
                                                                   f"//*[@id='root']/div/div[2]/div/div/div[2]/div[{e}]/div[1]/div/div[{i}]/div/div/ul/li[{j}]/div/div/a").get_attribute(
                                'href')
                            photos = self.driver.find_element('xpath',
                                                              f"//*[@id='root']/div/div[2]/div/div/div[2]/div[{e}]/div[1]/div/div[{i}]/div/div/ul/li[{j}]/div/div/a/div/div[1]/figure/img").get_attribute(
                                'src')
                            print(k, name.text, price.text, product_url, photos)
                            data = {}
                            data["category"] = k
                            data["name"] = name.text
                            data["price"] = price.text
                            data["product_url"] = product_url
                            data["photos"] = photos

                            res.append(data)
                # print(f'本頁獲取的結果：{json.dumps(res)}')
                # return res

            except Exception as e:
                print(e)
                # continue用來爬完該分類後繼續執行下一個分類
                # continue
            finally:
                print('本頁獲取的JSON：{}'.format(json.dumps(res, ensure_ascii=False)))
                self.save_mongodb(res)
                # return json.dumps(res, ensure_ascii=False)

    def get_category(self):
        self.url = "https://shop.pxmart.com.tw/v2/official/SalePageCategory/0?sortMode=Newest"
        self.driver.implicitly_wait(5)
        # 打開網址
        self.driver.get(self.url)
        for i in range(8, 40):
            all_category_name = self.driver.find_element('xpath',
                                                         f"//*[@id='root']/div/div[2]/div/div/div[1]/div/div[{i}]/div/div[1]/a")
            all_category_url = self.driver.find_element('xpath',
                                                        f"//*[@id='root']/div/div[2]/div/div/div[1]/div/div[{i}]/div/div[1]/a").get_attribute(
                'href')
            all_category_num = all_category_url.replace("https://shop.pxmart.com.tw/v2/official/SalePageCategory/", "")
            print(all_category_name.text, all_category_num)

    def save_mongodb(self, data):
        # 將爬取的資料存入mongodb
        client = pymongo.MongoClient(host='mongodb+srv://admin:00065638@cluster0.fiqpaqd.mongodb.net/?retryWrites=true&w=majority', port=27017)
        db = client["test"]
        collection = db.pxmart_product
        collection.insert_many(data)
    #     return


if __name__ == '__main__':
    start = datetime.datetime.now()
    pxmart = Pxmart()

    # 所有分類以及url
    #     dict_px_category = {"fresh_food":[240, 241, 374, 242, 255, 243], "frozen_food":[245], "drink_snacks":[244, 248, 250], "rice_oil_powder":[729, 246, 247, 249], "make_up":[252, 528], "baby":[441], "life_style":[254, 222, 358], "daily_use":[251, 253, 511], "furniture":[518], "clothing":[462, 522, ], "electrical":[497, 502, 506]}
    dict_px_category = {"frozen_food":[245], "drink_snacks":[244, 248, 250], "rice_oil_powder":[729, 246, 247, 249], "make_up":[252, 528], "baby":[441], "life_style":[254, 222, 358], "daily_use":[251, 253, 511], "furniture":[518], "clothing":[462, 522, ], "electrical":[497, 502, 506]}
    # 用dict的items()方法取出key和value  代入get_content()方法
    for k, v in dict_px_category.items():
        for i in v:
            print(k, i)
            pxmart.get_content(k, i)
    end = datetime.datetime.now()
    print("執行時間：", end - start)
