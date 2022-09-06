import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import os
when = time.strftime("%Y-%m-%d")


#爬非生鮮、非冷凍商品的函數
def RT_Mart():
    product_list = pd.DataFrame({})
    product_id = {
        "drink_snacks":[3793,3794,4051,4052,4053,4058,127808,127983,3742,130048],
        "rice_oil_powder":[3737,4050,4065,3799,3801,128298,167570,168795],
        "make_up":[76476,76510,31822,47284,25790,25829,4123,4124,25673,25686,25725,25530,25543,3810,73550,132499,132709],
        "baby":[3800,3745],
        "life_style":[3747,162670,28741,30964,74572,14001,169775,169845,30171],
        "daily_use":[3746,3738,132884,150140,150700,154130,162250,28663,169565,169670,133059],
        "furniture":[132849,132954,133409,134739,135089,25127,25140,25153,25478,169530,169635],
        "clothing":[3736],
        "electrical":[71505,3749,169740,104458],
        "3C":[3750]
    }
    
    for k in product_id.keys():
        product_name = []
        product_price = []
        product_url_list = []
        photos = []

        for v in product_id[k]:
            p=1
            while p >= 1:
                product_url = f"https://www.rt-mart.com.tw/direct/index.php?action=product_sort&prod_sort_uid={v}&prod_size=&p_data_num=72&usort=&page={p}"
                xx = requests.session()
                xx.keep_alive = False
                xx.cookies.clear()
                requests.adapters.DEFAULT_RETRIES = 5
                
                a = xx.get(product_url).text
                b = BeautifulSoup(a,"html.parser")
                product_72_url = b.select("div.for_imgbox a")

                yy = requests.session()
                yy.keep_alive = False
                xx.cookies.clear()
                requests.adapters.DEFAULT_RETRIES = 5
                
                try:
                    for i in range(0,72):

                        #取商品網址
                        product_1_url = product_72_url[i]["href"]
                        product_url_list.append(product_1_url)


                        #去掉多餘的字、取名稱
                        c = yy.get(product_1_url).text
                        d = BeautifulSoup(c,"html.parser")
                        remove_useless = d.select("span#prod_title.h2")[0].text

                        remove_useless = remove_useless.replace("/","-")
                        if remove_useless[0] == "*":
                            remove_useless = remove_useless.replace("*","",1)
                        remove_useless = remove_useless.replace("\t","")
                        remove_useless = remove_useless.replace("'","")
                        remove_useless = remove_useless.replace("<","")
                        remove_useless = remove_useless.replace(">","")
                        remove_useless = remove_useless.replace("?","")
                        remove_useless = remove_useless.replace("*","x")
                        remove_useless = remove_useless.replace(":","對")
                        remove_useless = remove_useless.replace("\\"," ")
                        remove_useless = remove_useless.replace("\""," ")

                        if remove_useless not in product_name:
                            product_name.append(remove_useless)
                        elif remove_useless in product_name:
                            repeat_list = []
                            for pn in product_name:
                                try:
                                    fix_repeat_name = remove_useless.replace("(","\\(")
                                    fix_repeat_name = fix_repeat_name.replace(")","\\)")
                                    repeat_name = re.search(fix_repeat_name,pn).group()
                                    repeat_list.append(repeat_name)
                                except:
                                    pass
                            repeat_num = len(repeat_list) + 1
                            remove_useless = remove_useless + str(repeat_num)
                            product_name.append(remove_useless)


                        #取圖片網址
                        product_pic_url = d.select("img#item_img")[0]["src"]
                        photos.append(product_pic_url)


                        #取價格
                        product_price_fix = d.select("span.price_num")[0].text
                        product_price_fix = product_price_fix.strip("$")
                        product_price_fix = product_price_fix.split()[0]
                        product_price.append(int(product_price_fix))

                        print(k,v,p,i,(i+1)+(p-1)*72,remove_useless)

                    p+=1

                except:
                    break
        
        #做表格                         
        product_list_category = pd.DataFrame({
            "category":k,
            "date":when,
            "market":"RT-Mart",
            "price":product_price,
            "product_name":product_name,
            "product_url":product_url_list,
            "photos":photos
        })
        
        product_list = pd.concat([product_list,product_list_category],ignore_index=True)

    mongo_data = product_list.to_dict('records')
    return mongo_data



#爬生鮮、冷凍商品的函數
def RT_Mart_ff():
    ff_list = pd.DataFrame({})
    store = {
        "nh2":"台北內湖2店",
        "tucheng":"新北土城店",
        "bitan":"新北碧潭店",
        "pingchen":"桃園平鎮店",
        "zhongxiao":"新竹忠孝店",
        "toufen":"苗栗頭份店",
        "tainan":"台南台南店",
        "fongshan":"高雄鳳山店",
        "taitung":"台東台東店"
    }

    fresh_food_id = {
        "nh2":[73929,5572,5573],
        "tucheng":[73938,32633,32634],
        "bitan":[73930,6331,6332],
        "pingchen":[73940,36113,36114],
        "zhongxiao":[73931,7090,7091],
        "toufen":[73941,38605,38606],
        "tainan":[73936,19304,19305],
        "fongshan":[73939,34373,34374],
        "taitung":[73937,23369,23370]
    }

    frozen_food_id = {
        "nh2":[73963],
        "tucheng":[73972],
        "bitan":[73964],
        "pingchen":[73974],
        "zhongxiao":[73965],
        "toufen":[73975],
        "tainan":[73970],
        "fongshan":[73973],
        "taitung":[73971]
    }

    product_type = [
        "fresh_food",
        "frozen_food"
    ]

    product_id = [
        fresh_food_id,
        frozen_food_id
    ]

    
    for ff in product_type:
        for pi in product_id:
            if product_id.index(pi) != product_type.index(ff):
                pass
            else:
                for k in pi.keys():
                    ff_name = []
                    ff_price = []
                    ff_url_list = []
                    ff_photos = []
                    for v in pi[k]:
                        p=1
                        while p >= 1:
                            ff_url = f"https://www.rt-mart.com.tw/{k}/index.php?action=product_sort&prod_sort_uid={v}&prod_size=&p_data_num=72&usort=&page={p}"
                            xx = requests.session()
                            xx.keep_alive = False
                            xx.cookies.clear()
                            requests.adapters.DEFAULT_RETRIES = 5

                            a = xx.get(ff_url).text
                            b = BeautifulSoup(a,"html.parser")
                            ff_72_url = b.select("div.for_imgbox a")

                            yy = requests.session()
                            yy.keep_alive = False
                            yy.cookies.clear()
                            requests.adapters.DEFAULT_RETRIES = 5

                            try:
                                for i in range(0,72):

                                    #取商品網址
                                    ff_1_url = ff_72_url[i]["href"]
                                    ff_url_list.append(ff_1_url)


                                    #去掉多餘的字、取名稱
                                    c = yy.get(ff_1_url).text
                                    d = BeautifulSoup(c,"html.parser")
                                    remove_useless = d.select("span#prod_title.h2")[0].text

                                    remove_useless = remove_useless.replace("/","-")
                                    if remove_useless[0] == "*":
                                        remove_useless = remove_useless.replace("*","",1)
                                    remove_useless = remove_useless.replace("\t","")
                                    remove_useless = remove_useless.replace("'","")
                                    remove_useless = remove_useless.replace("<","")
                                    remove_useless = remove_useless.replace(">","")
                                    remove_useless = remove_useless.replace("?","")
                                    remove_useless = remove_useless.replace("*","x")
                                    remove_useless = remove_useless.replace(":","對")
                                    remove_useless = remove_useless.replace("\\"," ")
                                    remove_useless = remove_useless.replace("\""," ")
                                    remove_useless = store[k] + "_" + remove_useless
                                    
                                    if remove_useless not in ff_name:
                                        ff_name.append(remove_useless)
                                    elif remove_useless in ff_name:
                                        repeat_list = []
                                        for mn in ff_name:
                                            try:
                                                fix_repeat_name = remove_useless.replace("(","\\(")
                                                fix_repeat_name = fix_repeat_name.replace(")","\\)")
                                                fix_repeat_name = fix_repeat_name.replace("+","\\+")
                                                fix_repeat_name = fix_repeat_name + "[^*]"
                                                repeat_name = re.search(fix_repeat_name,mn).group()
                                                repeat_list.append(repeat_name)
                                            except:
                                                pass
                                            
                                        repeat_num = len(repeat_list) + 1
                                        remove_useless = remove_useless + str(repeat_num)
                                        ff_name.append(remove_useless)
                                

                                    #取圖片網址
                                    ff_pic_url = d.select("img#item_img")[0]["src"]
                                    ff_photos.append(ff_pic_url)


                                    #取價格
                                    ff_price_fix = d.select("span.price_num")[0].text
                                    ff_price_fix = ff_price_fix.strip("$")
                                    ff_price_fix = ff_price_fix.split()[0]
                                    ff_price.append(int(ff_price_fix))

                                    print(ff,k,v,p,i,(i+1)+(p-1)*72,remove_useless)
                                
                                p+=1

                            except:
                                break

                    ff_list_category = pd.DataFrame({
                        "category":ff,
                        "date":when,
                        "market":"RT-Mart",
                        "price":ff_price,
                        "product_name":ff_name,
                        "product_url":ff_url_list,
                        "photos":ff_photos
                    })

                    global ff_list
                    ff_list = pd.concat([ff_list,ff_list_category],ignore_index=True)

    mongo_data = ff_list.to_dict('records')
    return mongo_data