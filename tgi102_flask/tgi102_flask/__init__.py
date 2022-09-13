from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from flask import request, render_template
from flask_paginate import Pagination, get_page_parameter


app = Flask(__name__)

from tgi102_flask.config import Config

db = SQLAlchemy()
BASE = declarative_base()
db.init_app(app)