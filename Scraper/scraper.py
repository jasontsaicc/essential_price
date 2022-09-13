import px_request as p
import rtmart as r
import Carrefour_test_1 as c
import scraper_to_mongodb as m
import pymongo
from pymongo import MongoClient
import datetime


client = MongoClient('mongodb+srv://admin:tgi102aaa@cluster0.19rsmeq.mongodb.net/?retryWrites=true&w=majority')
db = client.All_Market

# pxmart scraper
px = p.Pxmart()
dict_px_category = {"fresh_food":[240, 241, 374, 242, 255, 243], "frozen_food":[245], "drink_snacks": [244, 248, 250], 
                    "rice_oil_powder": [729, 246, 247, 249], "make_up": [252, 528], "baby": [441], 
                    "life_style": [254, 222, 358], "daily_use": [251, 253, 511], "furniture": [518], "clothing": [462, 522],
                    "electrical": [497, 502, 506]}
for category_key, category_values in dict_px_category.items():
    for category_value in category_values:
        px_data = px.get_content(category_key, category_value)
        m.pxmart(px_data)

# rt-mart scraper
rt_data = r.RT_Mart()
rt_ff_data = r.RT_Mart_ff()
m.rtmart(rt_data)
m.rtmart(rt_ff_data)

# carrefour scraper
url_list = ["https://online.carrefour.com.tw/zh/%E7%94%9F%E9%AE%AE%E9%A3%9F%E5%93%81?start={}#",  # 生鮮食品
            "https://online.carrefour.com.tw/zh/%E5%86%B7%E5%87%8D%E9%A3%9F%E5%93%81?start={}#",  # 冷凍食品
            "https://online.carrefour.com.tw/zh/%E9%A3%B2%E6%96%99%E9%9B%B6%E9%A3%9F?start={}#", # 零食飲料
            "https://online.carrefour.com.tw/zh/%E7%B1%B3%E6%B2%B9%E6%B2%96%E6%B3%A1?start={}#",  # 米油沖泡
            "https://online.carrefour.com.tw/zh/%E7%BE%8E%E5%A6%9D%E8%AD%B7%E7%90%86?start={}#",  # 美妝護理
            "https://online.carrefour.com.tw/zh/%E6%AF%8D%E5%AC%B0%E4%BF%9D%E5%81%A5?start={}#",  # 嬰兒
            "https://online.carrefour.com.tw/zh/%E7%94%9F%E6%B4%BB%E4%BC%91%E9%96%92?start={}#",  # 生活休閒
            "https://online.carrefour.com.tw/zh/%E6%97%A5%E7%94%A8%E7%99%BE%E8%B2%A8?start={}#",  # 日用百貨
            "https://online.carrefour.com.tw/zh/%E5%82%A2%E4%BF%B1%E5%AF%A2%E9%A3%BE?start={}#",  # 家具
            "https://online.carrefour.com.tw/zh/%E6%9C%8D%E9%A3%BE%E9%9E%8B%E5%8C%85?start={}#",  # 服飾
            "https://online.carrefour.com.tw/zh/%E5%A4%A7%E5%B0%8F%E5%AE%B6%E9%9B%BB?start={}#",  # 家電
            "https://online.carrefour.com.tw/zh/3c?start={}#"] 
ca = c.main()
for category in url_list:
  ca_data = ca.get_ALLproduction(category)
  m.carr(ca_data)
