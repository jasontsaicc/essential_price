import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
when = time.strftime("%Y-%m-%d")

#爬非生鮮、非冷凍商品的函數
def RT_Mart(k,v):
    product_name = []
    product_price = []
    product_url_list = []
    photos = []
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
    product_list = pd.DataFrame({
        "category":k,
        "date":when,
        "market":"RT-Mart",
        "price":product_price,
        "product_name":product_name,
        "product_url":product_url_list,
        "photos":photos
    })
        
    mongo_data = product_list.to_dict('records')
    return mongo_data










#爬生鮮、冷凍商品的函數
def RT_Mart_ff(ff,k,v,store):
    ff_name = []
    ff_price = []
    ff_url_list = []
    ff_photos = []
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

    ff_list = pd.DataFrame({
        "category":ff,
        "date":when,
        "market":"RT-Mart",
        "price":ff_price,
        "product_name":ff_name,
        "product_url":ff_url_list,
        "photos":ff_photos
    })

    mongo_data = ff_list.to_dict('records')
    return mongo_data
