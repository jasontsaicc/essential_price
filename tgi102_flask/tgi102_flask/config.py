from . import app
import os

config_path = os.path.abspath(os.path.dirname(__file__))
print(config_path)


class Config:
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:00065638@34.80.145.135/essential"
