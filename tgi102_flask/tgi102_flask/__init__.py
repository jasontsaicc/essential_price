from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from flask import request, render_template, redirect, url_for
from flask_paginate import Pagination, get_page_parameter
from flask_msearch import Search

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://admin:tgi102aaa@projectdb.ckq7h3eivlb4.ap-northeast-1.rds.amazonaws.com:3306/essential"
    app.config['UPLOAD_FOLDER'] = "tgi102_flask/static/upload/"
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

    db.init_app(app)
    search = Search()
    search.init_app(app)
    search.create_index()
    app.app_context().push()

    return app


app = create_app()
# app.app_context().push()

# from tgi102_flask.config import Config
BASE = declarative_base()
# db.init_app(app)

Session = sessionmaker(bind=db.engine)
session = Session()
