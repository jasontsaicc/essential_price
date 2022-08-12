from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import datetime
import time
from selenium.webdriver import Chrome, ChromeOptions
import pymongo


class Pxmart:
    # 初始化
    def __init__(self):
        self.url = None
        # 這裡可以設定要不要跑出瀏覽器出來 True 不顯示 False 顯示
        self.headless = ChromeOptions()
        self.headless.headless = True
        # 不加載圖片,加快訪問速度
        self.headless.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        # 此步驟很重要，設置為開發者模式，防止被各大網站識別出來使用了Selenium
        self.headless.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 使用Chrome瀏覽器 後面會換成
        self.driver = webdriver.Chrome("./chromedriver", options=self.headless)

    # 使用del 讓程式結束的時候關閉瀏覽器
    def __del__(self):
        self.driver.close()

    def get_content(self, category_url):
        # 這裡傳入分類數字的list
        for i in category_url:
            self.url = f'https://shop.pxmart.com.tw/v2/official/SalePageCategory/{i}'
            # 開啟網頁等待網頁載入完成
            self.driver.implicitly_wait(5)
            # 打開網址
            self.driver.get(self.url)
            time.sleep(2)
            try:
                # 這裡設置3層for迴圈 一欄4個商品 跑25行會xpath前面的值會改變 所以外面再加個迴圈 這樣理論可以跑一個分類800樣商品
                for e in range(2, 10):
                    for i in range(1, 25):
                        js = "window.scrollTo(0,document.body.scrollHeight)"
                        self.driver.execute_script(js)
                        # time.sleep(0.2)
                        for j in range(1, 5):
                            category = self.driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div/ol/li[2]/a/h1")
                            name = self.driver.find_element_by_xpath(
                                f"//*[@id='root']/div/div[2]/div/div/div[2]/div[{e}]/div[1]/div/div[{i}]/div/div/ul/li[{j}]/div/div/a/div/div[2]/div[1]")
                            price = self.driver.find_element_by_xpath(
                                f"//*[@id='root']/div/div[2]/div/div/div[2]/div[{e}]/div[1]/div/div[{i}]/div/div/ul/li[{j}]/div/div/a/div/div[2]/div[2]/div[1]/div[2]")
                            # 這裡是用get_attribute 可以爬出屬性值
                            product_url = self.driver.find_element_by_xpath(
                                f"//*[@id='root']/div/div[2]/div/div/div[2]/div[{e}]/div[1]/div/div[{i}]/div/div/ul/li[{j}]/div/div/a").get_attribute(
                                'href')
                            photos = self.driver.find_element_by_xpath(
                                f"//*[@id='root']/div/div[2]/div/div/div[2]/div[{e}]/div[1]/div/div[{i}]/div/div/ul/li[{j}]/div/div/a/div/div[1]/figure/img").get_attribute(
                                'src')
                            print(category.text, name.text, price.text, product_url, photos)

            except Exception as e:
                print(e)
                # continue用來爬完該分類後繼續執行下一個分類
                continue

    def get_category(self):
        self.url = "https://shop.pxmart.com.tw/v2/official/SalePageCategory/0?sortMode=Newest"
        self.driver.implicitly_wait(5)
        # 打開網址
        self.driver.get(self.url)
        for i in range(8, 40):
            all_category_name = self.driver.find_element_by_xpath(
                f"//*[@id='root']/div/div[2]/div/div/div[1]/div/div[{i}]/div/div[1]/a")
            all_category_url = self.driver.find_element_by_xpath(
                f"//*[@id='root']/div/div[2]/div/div/div[1]/div/div[{i}]/div/div[1]/a").get_attribute('href')
            all_category_num = all_category_url.replace("https://shop.pxmart.com.tw/v2/official/SalePageCategory/", "")
            print(all_category_name.text, all_category_num)

    def save_csv(self):
        pass
        # 改用pandas 寫入csv
        # df = pd.DataFrame({
        #     'category': [category.text],
        #     'product_name': [name.text],
        #     'price': [price.text],
        #     'product_url': [product_url],
        #     'photos': [photos]
        # })
        # # print(df)
        # df.to_csv('./pxmart.csv', mode='a', header=False, index=False)

    # with open('px_request.csv', 'a', encoding='utf-8') as f:
    #     f.write(category.text + ',' + name.text + ',' + price.text + ',' + product_url + ',' + photos + '\n')

    def save_pymongo(self):
        pass
        # myclient = pymongo.MongoClient(host='localhost', port=27017)
        # db = myclient['test']
        # collection = db.pxmart


if __name__ == '__main__':
    start = datetime.datetime.now()

    pxmart = Pxmart()
    px_category = [244]
    pxmart.get_category()
    # pxmart.get_content(px_category)

    end = datetime.datetime.now()
    print("執行時間：", end - start)

