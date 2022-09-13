from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient

import datetime
import pymongo
import json
import time


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
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

    # 使用del 讓程式結束的時候關閉瀏覽器
    def __del__(self):
        self.driver.close()

    def get_content(self, k, category_url):
        # 這裡傳入分類數字的url
        self.url = f'https://shop.pxmart.com.tw/v2/official/SalePageCategory/{category_url}'
        # 開啟網頁等待網頁載入完成
        self.driver.implicitly_wait(5)
        # 打開網址
        self.driver.get(self.url)
        time.sleep(2)
        try:
            result = []
            # 這裡設置3層for迴圈 一欄4個商品 跑25行會xpath前面的值會改變 所以外面再加個迴圈 這樣理論可以跑一個分類800樣商品
            for next_page in range(2, 10):
                for column in range(1, 25):
                    # 寫入JS代碼 自動移動到頁尾
                    js = "window.scrollTo(0,document.body.scrollHeight)"
                    self.driver.execute_script(js)
                    for row in range(1, 5):
                        # category = self.driver.find_element('xpath', f"//*[@id='root']/div/div[2]/div/ol/li[2]/a/h1")
                        name = self.driver.find_element('xpath',
                                                        f"//*[@id='root']/div/div[2]/div/div/div[2]/div[{next_page}]/div[1]/div/div[{column}]/div/div/ul/li[{row}]/div/div/a/div/div[2]/div[1]")
                        price = self.driver.find_element('xpath',
                                                         f"//*[@id='root']/div/div[2]/div/div/div[2]/div[{next_page}]/div[1]/div/div[{column}]/div/div/ul/li[{row}]/div/div/a/div/div[2]/div[2]/div[1]/div[2]")
                        # 這裡是用get_attribute 可以爬出屬性值
                        product_url = self.driver.find_element('xpath',
                                                               f"//*[@id='root']/div/div[2]/div/div/div[2]/div[{next_page}]/div[1]/div/div[{column}]/div/div/ul/li[{row}]/div/div/a").get_attribute(
                            'href')
                        photos = self.driver.find_element('xpath',
                                                          f"//*[@id='root']/div/div[2]/div/div/div[2]/div[{next_page}]/div[1]/div/div[{column}]/div/div/ul/li[{row}]/div/div/a/div/div[1]/figure/img").get_attribute(
                            'src')

                        print(category_url, k, datetime.date.today(), "PxMart", name.text, int(price.text.strip("NT$").replace(",", "")), product_url,
                              photos)

                        data = {"category": k, "date": str(datetime.date.today()), "market": "P",
                                "price": int(price.text.strip("NT$").replace(",", "")), "product_name": name.text, "product_url": product_url,
                                "photos": photos}
                        result.append(data)

        except Exception as e:
            print(e)

    def get_category(self):
        self.url = "https://shop.pxmart.com.tw/v2/official/SalePageCategory/0?sortMode=Newest"
        self.driver.implicitly_wait(5)
        # 打開網址
        self.driver.get(self.url)
        for category in range(8, 40):
            all_category_name = self.driver.find_element('xpath',
                                                         f"//*[@id='root']/div/div[2]/div/div/div[1]/div/div[{category_value}]/div/div[1]/a")
            all_category_url = self.driver.find_element('xpath',
                                                        f"//*[@id='root']/div/div[2]/div/div/div[1]/div/div[{category_value}]/div/div[1]/a").get_attribute(
                'href')
            all_category_num = all_category_url.replace("https://shop.pxmart.com.tw/v2/official/SalePageCategory/", "")
            print(all_category_name.text, all_category_num)
