import datetime
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pymongo
from pymongo import MongoClient
import time

# sleep_time = random.randint(1, 5)
# client = MongoClient(host="localhost", port=27017)
# db = client.admin
# collection = db['test']
# print(collection)
class main:
#     def __init__(self):
#         self.option = Options()
#         self.option.add_argument('headless')  # 啟動無頭模式
#         self.option.add_argument('disable-gpu')  # windows必須加入此行
#         self.driver = webdriver.Chrome(options=self.option)
# #         self.driver = webdriver.Chrome()
    # 使用del 讓程式結束的時候關閉瀏覽器
    # def __del__(self):
    #     self.driver.close()
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
#         self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)

    def get_ALLproduction(self, category, num_production):

        # url_list = ["https://online.carrefour.com.tw/zh/%E7%94%9F%E9%AE%AE%E9%A3%9F%E5%93%81?start={}#",  # 生鮮食品
        #             "https://online.carrefour.com.tw/zh/%E5%86%B7%E5%87%8D%E9%A3%9F%E5%93%81?start={}#"]  # 冷凍食品
                    # "https://online.carrefour.com.tw/zh/%E9%A3%B2%E6%96%99%E9%9B%B6%E9%A3%9F?start={}#",  # 零食飲料
                    # "https://online.carrefour.com.tw/zh/%E7%B1%B3%E6%B2%B9%E6%B2%96%E6%B3%A1?start={}#",  # 米油沖泡
                    # "https://online.carrefour.com.tw/zh/%E7%BE%8E%E5%A6%9D%E8%AD%B7%E7%90%86?start={}#",  # 美妝護理
                    # "https://online.carrefour.com.tw/zh/%E6%AF%8D%E5%AC%B0%E4%BF%9D%E5%81%A5?start={}#",  # 嬰兒
                    # "https://online.carrefour.com.tw/zh/%E7%94%9F%E6%B4%BB%E4%BC%91%E9%96%92?start={}#",  # 生活休閒
                    # "https://online.carrefour.com.tw/zh/%E6%97%A5%E7%94%A8%E7%99%BE%E8%B2%A8?start={}#",  # 日用百貨
                    # "https://online.carrefour.com.tw/zh/%E5%82%A2%E4%BF%B1%E5%AF%A2%E9%A3%BE?start={}#",  # 家具
                    # "https://online.carrefour.com.tw/zh/%E6%9C%8D%E9%A3%BE%E9%9E%8B%E5%8C%85?start={}#",  # 服飾
                    # "https://online.carrefour.com.tw/zh/%E5%A4%A7%E5%B0%8F%E5%AE%B6%E9%9B%BB?start={}#",  # 家電
                    # "https://online.carrefour.com.tw/zh/3c?start={}#"]  # 3C
        # date_time = datetime.datetime.now()
        # update = date_time.date()
        update = datetime.date.today()  # 取得抓取的日期
        # production = ['fresh_food', 'frozen_food', 'drink_snacks', 'rice_oil_powder', 'make_up', 'baby', 'life_style',
        #               'daily_use', 'furniture', 'clothing', 'electrical', '3C']
        all_product = []
        # for i in url_list:
        num = 0  # 觀察每個網址的第一頁start=0
        while True:
            try:
                for e in (1, 200):  # 跑幾頁
                    self.driver.get(num_production.format(num))
                    self.driver.implicitly_wait(0.5)
                    self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                    self.driver.implicitly_wait(0.5)
                    for j in range(0, 24):  # 每一頁有24個商品 [j] 第j個商品
                        names = self.soup.select('div[class="commodity-desc"] a')[j].text
                        name = str(names)
                        self.driver.implicitly_wait(0.5)
                        prices = self.soup.select('div[class="current-price"] em')[j].text
                        self.driver.implicitly_wait(0.5)
                        price = prices.strip('$')
                        self.driver.implicitly_wait(0.5)
                        pic = self.soup.select('div[class="box-img"] a.gtm-product-alink img.m_lazyload')[j].get('src')  # 用get 取src裡面的屬性
                        product_url = 'https://online.carrefour.com.tw' + str(self.soup.select('div[class="desc-operation-wrapper"] div[class="commodity-desc"] a')[j].get('href'))
                        try:
                            count = self.soup.select('div[class="box-img"] span.packageQty')[j].text  # 不是每個商品都是單一的 所以 不設try except 的話會有 IndexError
                            data = {"Category": category,
                                    'Data': str(update),
                                    "Market": "Carefour",
                                    "Price": price,
                                    "Product_name": name + ' ' + str(count),
                                    "PicUrl": pic,
                                    "Url": product_url}
                            print(data)
                            all_product.append(data)

                        except IndexError as I:
                            data = {"Category": category,
                                    'Data': str(update),
                                    "Market": "Carefour",
                                    "Price": price,
                                    "Product_name": names,
                                    "PicUrl": pic,
                                    'Url': product_url}
                            print(data)
                            all_product.append(data)
                            continue
                    num += 24
                    # return all_product
            except IndexError as I:
                    break
            # collection.insert_many(all_product)
            # print(all_product)
            # print("=======================================")
#         self.driver.close()
        return all_product
# if __name__ == '__main__':
#     carrefour = main()
#     carrefour.get_ALLproduction()





