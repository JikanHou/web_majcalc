from flask import Flask, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import pymysql
pymysql.install_as_MySQLdb()
app = Flask("majcalc")
app.config.from_pyfile("settings.py")
bootstrap = Bootstrap5(app)
loginManager = LoginManager(app)
db = SQLAlchemy(app)
loginManager.login_view = "/login"
loginManager.login_message = "登录以访问此界面"
from majcalc import views, models, forms, commands, extensions
db.create_all()