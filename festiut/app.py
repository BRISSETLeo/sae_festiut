from flask import Flask
from flask_bootstrap import Bootstrap5
import os.path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

def mkpath(p):
    return os.path. normpath (os.path.join(os.path. dirname ( __file__ ), p))

app = Flask( __name__ )
bootstrap = Bootstrap5(app)
login_manager = LoginManager(app)

app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SECRET_KEY'] = '3b6be466-1cd7-47cc-9a61-689735e10610'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ozocak:ozocak@servinfo-maria:3306/DBozocak'

db = SQLAlchemy(app)