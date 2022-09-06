import px_request as p
import rtmart as r
import carrefour as c
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
ca = c.main()
ca_data = ca.get_ALLproduction()
m.carr(ca_data)
