import jieba
import re
import mysql.connector
from mysql.connector import errorcode

# MySQL connection
config = {
  'host':'projectdb.ckq7h3eivlb4.ap-northeast-1.rds.amazonaws.com',
  'user':'admin',
  'password':'tgi102aaa',
  'database':'essential'
}

conn = mysql.connector.connect(**config)
print("Connection established")
cursor = conn.cursor()

# 使用Jieba分詞處理使用者輸入的商品名稱
text = "五月花衛生紙"
letter = list(jieba.cut(text, cut_all=False, HMM=True))
print(letter)

# SQL select & 處理回傳結果格式
sql_cmd = f"""
        select 
            pd.product_name, 
            pr.price
        from product pd
            join price pr
                on pd.id = pr.product_id
        where 
            pd.product_name regexp '[{text}]' and pr.`date` = '2022-08-24'
        """

cursor.execute(sql_cmd)
product = cursor.fetchall()
product_list = []
for row in product:
    row = list(row)
    product_list.append(row)

# SQL查詢結果之商品名，需達到Jieba分詞結果之40%符合程度，才回傳該項商品資訊
return_list = []
for j in product_list:
    percent = len(letter) * 0.4
    n = 0
    for i in letter:
        pattern0 = re.compile((letter[0]))
        compare0 = pattern0.search(j[0])
        if compare0 is None:
            break
        else:
            pattern = re.compile((i))
            compare = pattern.search(j[0])
            if compare is not None:
                if n >= percent and j not in return_list:
                    return_list.append(j)
                n += 1

print(return_list)