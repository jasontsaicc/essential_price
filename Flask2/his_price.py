from flask import Flask
from flask import render_template
import matplotlib.pyplot as plt
import io
import base64
from flask_sqlalchemy import SQLAlchemy
import numpy as np



app = Flask(__name__)

plt.rcParams['font.sans-serif']=['Microsoft JhengHei'] #用来顯示中文
plt.rcParams['axes.unicode_minus']=False #用来顯示負號
plt.rcParams['font.weight'] = 'bold'

# setting MySQL
db = SQLAlchemy()
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://admin:tgi102aaa@projectdb.ckq7h3eivlb4.ap-northeast-1.rds.amazonaws.com:3306/essential"

db.init_app(app)
product = '老欉文旦家庭號'
marts = 'P'

def history_conSQL():

    sql_cmd = f"""
        SELECT * FROM(
        SELECT 
            concat(date_format(`date`, '%%m'),'/',date_format(`date`, '%%d'))as pd_date ,price 
        FROM(
            product pd
	            join price pr
		            on pd.id = pr.product_id)
			            join marts mr
				            on pd.mart_id = mr.id
		WHERE
	        pd.product_name like '%%{product}%%' and mr.id = "{marts}" 
        ORDER BY
            1 desc
        LIMIT
            10) as his_pr
        ORDER BY
            1 asc
        
        """
    query_data = db.engine.execute(sql_cmd)
    rows_date = list()
    rows_price = list()
    for row in query_data:
        print("row:", row[0], row[1])
        rows_date.append(row[0])  
        rows_price.append(row[1])

    return rows_date, rows_price

@app.route('/')
def build_plot():
    img = io.BytesIO()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    fig.suptitle('歷史價格圖', fontsize=14, fontweight='bold')
    ax.set_xlabel("日期")
    ax.set_ylabel("價格          ", rotation=0)
    da_list, pr_list = history_conSQL()

    plt.plot(da_list, pr_list)
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('plot.html', plot_url=plot_url)


if __name__ == '__main__':
    app.debug = True
    app.run()
