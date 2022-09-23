import px_request as p
import rtmart as r
import Carrefour_test_1 as c
import scraper_to_mongodb as m
import pymongo
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import datetime

client = MongoClient('mongodb+srv://admin:tgi102aaa@cluster0.19rsmeq.mongodb.net/?retryWrites=true&w=majority')
db = client.All_Market

# pxmart scraper
# px = p.Pxmart()
# dict_px_category = {"fresh_food":[240, 241, 374, 242, 255, 243], "frozen_food":[245], "drink_snacks": [244, 248, 250], 
#                     "rice_oil_powder": [729, 246, 247, 249], "make_up": [252, 528], "baby": [441], 
#                     "life_style": [254, 222, 358], "daily_use": [251, 253, 511], "furniture": [518], "clothing": [462, 522],
#                     "electrical": [497, 502, 506]}
# for category_key, category_values in dict_px_category.items():
#     for category_value in category_values:
#         px_data = px.get_content(category_key, category_value)
#         m.pxmart(px_data)


        
# carrefour scraper
dic_carrefour_category = {'fresh_food': 'https://online.carrefour.com.tw/zh/%E7%94%9F%E9%AE%AE%E9%A3%9F%E5%93%81?start={}#',
                          'frozen_food': 'https://online.carrefour.com.tw/zh/%E5%86%B7%E5%87%8D%E9%A3%9F%E5%93%81?start={}#',
                          'drink_snacks': 'https://online.carrefour.com.tw/zh/%E9%A3%B2%E6%96%99%E9%9B%B6%E9%A3%9F?start={}#',
                          'rice_oil_powder': 'https://online.carrefour.com.tw/zh/%E7%B1%B3%E6%B2%B9%E6%B2%96%E6%B3%A1?start={}#',
                          'make_up': 'https://online.carrefour.com.tw/zh/%E7%BE%8E%E5%A6%9D%E8%AD%B7%E7%90%86?start={}#',
                          'baby': 'https://online.carrefour.com.tw/zh/%E6%AF%8D%E5%AC%B0%E4%BF%9D%E5%81%A5?start={}#',
                          'life_style': 'https://online.carrefour.com.tw/zh/%E7%94%9F%E6%B4%BB%E4%BC%91%E9%96%92?start={}#',
                          'daily_use': 'https://online.carrefour.com.tw/zh/%E6%97%A5%E7%94%A8%E7%99%BE%E8%B2%A8?start={}#',
                          'furniture': 'https://online.carrefour.com.tw/zh/%E5%82%A2%E4%BF%B1%E5%AF%A2%E9%A3%BE?start={}#',
                          'clothing': 'https://online.carrefour.com.tw/zh/%E6%9C%8D%E9%A3%BE%E9%9E%8B%E5%8C%85?start={}#',
                          'electrical': 'https://online.carrefour.com.tw/zh/%E5%A4%A7%E5%B0%8F%E5%AE%B6%E9%9B%BB?start={}#',
                          '3C': 'https://online.carrefour.com.tw/zh/3c?start={}#',
                          }
ca = c.main()
for category in dic_carrefour_category:
    num_production = dic_carrefour_category[category]
    ca_data = ca.get_ALLproduction(category, num_production)
    m.carr(ca_data)        
        
        
# rt-mart scraper
# product_id = {
#     "drink_snacks":[3793,3794,4051,4052,4053,4058,127808,127983,3742,130048],
#     "rice_oil_powder":[3737,4050,4065,3799,3801,128298,167570,168795],
#     "make_up":[76476,76510,31822,47284,25790,25829,4123,4124,25673,25686,25725,25530,25543,3810,73550,132499,132709],
#     "baby":[3800,3745],
#     "life_style":[3747,162670,28741,30964,74572,14001,169775,169845,30171],
#     "daily_use":[3746,3738,132884,150140,150700,154130,162250,28663,169565,169670,133059],
#     "furniture":[132849,132954,133409,134739,135089,25127,25140,25153,25478,169530,169635],
#     "clothing":[3736],
#     "electrical":[71505,3749,169740,104458],
#     "3C":[3750]
# }
# for k in product_id.keys():
#     for v in product_id[k]:
#         rt_data = r.RT_Mart(k=k,v=v)
#         m.rtmart(rt_data)

        
# store = {
#     "nh2":"台北內湖2店",
#     "tucheng":"新北土城店",
#     "bitan":"新北碧潭店",
#     "pingchen":"桃園平鎮店",
#     "zhongxiao":"新竹忠孝店",
#     "toufen":"苗栗頭份店",
#     "tainan":"台南台南店",
#     "fongshan":"高雄鳳山店",
#     "taitung":"台東台東店"
# }

# fresh_food_id = {
#     "nh2":[73929,5572,5573],
#     "tucheng":[73938,32633,32634],
#     "bitan":[73930,6331,6332],
#     "pingchen":[73940,36113,36114],
#     "zhongxiao":[73931,7090,7091],
#     "toufen":[73941,38605,38606],
#     "tainan":[73936,19304,19305],
#     "fongshan":[73939,34373,34374],
#     "taitung":[73937,23369,23370]
# }

# frozen_food_id = {
#     "nh2":[73963],
#     "tucheng":[73972],
#     "bitan":[73964],
#     "pingchen":[73974],
#     "zhongxiao":[73965],
#     "toufen":[73975],
#     "tainan":[73970],
#     "fongshan":[73973],
#     "taitung":[73971]
# }

# product_type = [
#     "fresh_food",
#     "frozen_food"
# ]

# product_id = [
#     fresh_food_id,
#     frozen_food_id
# ]
# for ff in product_type:
#     for pi in product_id:
#         if product_id.index(pi) != product_type.index(ff):
#             pass
#         else:
#             for k in pi.keys():
#                 for v in pi[k]:
#                     rt_ff_data = r.RT_Mart_ff(ff=ff,k=k,v=v,store=store)
#                     m.rtmart(rt_ff_data)
