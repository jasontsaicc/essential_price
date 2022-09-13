from . import app
import os
import sqlalchemy as sa

config_path = os.path.abspath(os.path.dirname(__file__))
print(config_path)


class Config:
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://admin:tgi102aaa@projectdb.ckq7h3eivlb4.ap-northeast-1.rds.amazonaws.com:3306/essential"
