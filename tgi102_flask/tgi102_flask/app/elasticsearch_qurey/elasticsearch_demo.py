
import pymysql
import mysql.connector

from elasticsearch import Elasticsearch


def get_data():
    config = {
        'host': 'projectdb.ckq7h3eivlb4.ap-northeast-1.rds.amazonaws.com',
        'user': 'admin',
        'password': 'tgi102aaa',
        'database': 'essential',
    }
    conn = mysql.connector.connect(**config)
    print("Connection established")
    cursor = conn.cursor()

    sql_cmd = f"""select * from product pd join price pr on pd.id = pr.product_id"""
    cursor.execute(sql_cmd)
    results = cursor.fetchall()
    conn.close()
    return results


def create_es_data():
    es = Elasticsearch(hosts='127.0.0.1', port=9200)
    results = get_data()
    for row in results:
        # print("row", row)
        print("row[0]", row[0]),
        print("row[1]", row[1]),
        print("row[2]", row[2]),
        print("row[3]", row[3]),
        print("row[6]", row[6]),
        body={
            "id" : row[0],
            "product_name" : row[1],
            "product_url" : row[2],
            "pic_url" : row[3],
            "price" : row[6]
        }
        # print("message", body)
        es.index(index="essential", body=body)


if __name__=="__main__":
    create_es_data()