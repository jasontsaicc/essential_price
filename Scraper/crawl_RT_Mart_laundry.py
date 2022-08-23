# 爬取商品圖片、完整名稱、價格。
# 爬大潤發食用油、洗衣精、洗碗精、餅乾、調味料（如鹽、糖、醋、醬油、味精等）、泡麵
# 爬下來的商品依前述商品類別進行分類，並將資料存入csv檔
# csv檔欄位名稱及順序：商品類別、商品全名、商品價格
# 圖片檔存.jpg檔，檔名為賣場名稱_完整產品名稱
####### 需將爬蟲設定排程，每間隔固定時間，重新爬取商品資訊，取得最新的價格。（排程可於模型訓練完成後再設置）
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

laundry_name = []
laundry_price = []
url_list = []

p=1
while p >= 1:
    laundry_URL = f"https://www.rt-mart.com.tw/direct/index.php?action=product_sort&prod_sort_uid=4212&prod_size=&p_data_num=72&usort=&page={p}"
                

    xx = requests.session()
    xx.keep_alive = False
    xx.cookies.clear()
    requests.adapters.DEFAULT_RETRIES = 5
    a = xx.get(laundry_URL).text
    b = BeautifulSoup(a,"html.parser")
    first_page = b.select("div.for_imgbox a")
    
    
    yy = requests.session()
    yy.keep_alive = False
    xx.cookies.clear()
    requests.adapters.DEFAULT_RETRIES = 5
    try:
        for i in range(0,72):
            #取商品網址
            cc = first_page[i]["href"]
            url_list.append(cc)

            c = yy.get(cc).text
            d = BeautifulSoup(c,"html.parser")
    
    
            #取名稱、去掉多餘的字
            remove_useless = d.select("span#prod_title.h2")[0].text
            useless = "/*"
            for u in useless:
                if u == "/":
                    remove_useless = remove_useless.replace(u,"-")
                elif remove_useless[0] == "*":
                    remove_useless = remove_useless.replace(u,"")
                else:
                    remove_useless = remove_useless.replace(u,"x")

            if remove_useless not in laundry_name:
                laundry_name.append(remove_useless)
            elif remove_useless in laundry_name:
                repeat_list = []
                for ln in laundry_name:
                    try:
                        fix_repeat_name = remove_useless.replace("(","\\(")
                        fix_repeat_name = fix_repeat_name.replace(")","\\)")
                        repeat_name = re.search(fix_repeat_name,ln).group()
                        repeat_list.append(repeat_name)
                    except:
                        pass
                repeat_num = len(repeat_list) + 1
                laundry_name.append(remove_useless + str(repeat_num))

    
            #下載圖片
            laundry_pic_URL = d.select("img#item_img")[0]["src"]
            laundry_pic = requests.get(laundry_pic_URL).content
            laundry_pic_path = f"C:/Users/TibeMe_user/Desktop/project/product/laundry/大潤發_{laundry_name[i+(p-1)*72]}.jpg"
            with open(laundry_pic_path,"wb") as opc:
                opc.write(laundry_pic)
    
    
            #取價格
            laundry_price_fix = d.select("span.price_num")[0].text
            laundry_price_fix = laundry_price_fix.strip("$")
            laundry_price_fix = laundry_price_fix.split()[0]
            laundry_price.append(laundry_price_fix)
        
        p+=1
    
    except:
        #做表格
        laundry_name = pd.Series(laundry_name)
        laundry_price = pd.Series(laundry_price)
        when = time.strftime("%Y-%m-%d")
        laundry_list = pd.DataFrame(
            {"商品類別":"洗衣精",
            "商品全名":laundry_name,
            "商品價格":laundry_price,
            "價格更新時間":when,
            "商品網址":url_list})
        laundry_list.to_csv(f"C:/Users/TibeMe_user/Desktop/project/product/laundry/laundry_list_{when}.csv")
        break
