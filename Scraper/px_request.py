from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
import time


class Pxmart():

    # 初始化
    def __init__(self):
        # 這裡可以設定要不要跑出瀏覽器出來 True 不顯示 False 顯示
        self.headless = ChromeOptions()
        self.headless.headless = True
        self.url = 'https://shop.pxmart.com.tw/v2/official/SalePageCategory/251?sortMode=Sales'
        # 使用Chrome瀏覽器
        self.driver=webdriver.Chrome("./chromedriver", options=self.headless)

    # 使用del 讓程式結束的時候關閉瀏覽器
    def __del__(self):
        self.driver.close()

    def get_content(self):
        # 開啟網頁等待網頁載入完成
        self.driver.implicitly_wait(5)
        # 打開網址
        self.driver.get(self.url)
        # time.sleep(3)

        try:
            # 這裡設置3層for迴圈 一欄4個商品 跑25行會xpath前面的值會改變 所以外面再加個迴圈 這樣理論可以跑一個分類800樣商品
            for e in range(2, 10):
                for i in range(1, 25):
                    # 這裡的js 可以讓捲軸卷到底
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
                        print("類別: ", category.text, "品名: ", name.text, "價格: ", price.text, "產品網址: ", product_url, "照片網址: ",
                              photos)
                        # time.sleep(0.5)

                        with open('px_request.csv', 'a', encoding='utf-8') as f:
                            f.write(category.text + ',' + name.text + ',' + price.text + ',' + product_url + ',' + photos + '\n')
        except Exception as e:
            print(e)



    def save_csv(self):
        pass

if __name__ == '__main__':
    pxmart = Pxmart()
    pxmart.get_content()

