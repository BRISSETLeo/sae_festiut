from flask import Flask
import os.path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

def mkpath(p):
    return os.path. normpath (os.path.join(os.path. dirname ( __file__ ), p))

app = Flask( __name__ )
login_manager = LoginManager(app)

app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SECRET_KEY'] = '3b6be466-1cd7-47cc-9a61-689735e10610'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://nocros:53ea7CLG23z2TwkvkHGNi8u4GBd7s2X7@mysql-nocros.alwaysdata.net:3306/nocros_festiut'

db = SQLAlchemy(app)