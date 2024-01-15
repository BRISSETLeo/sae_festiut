from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bootstrap import Bootstrap5
import os.path
from flask_login import LoginManager

def mkpath(p):
    return os.path.normpath(os.path.join(os.path.dirname( __file__ ),p))

app = Flask( __name__ )

app.config['BOOTSTRAP_SERVE_LOCAL'] = True
bootstrap = Bootstrap5(app)

app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///'+mkpath('./myapp.db'))
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = "6cc5c628-bfc6-41eb-9307-94af8a63fd10"

login_manager = LoginManager(app)
login_manager.login_view = "login"

with app.app_context():
    db.create_all()

    import yaml

    from.models import Compte

    authors = {}
    o = Compte(pseudo="NoCros")
    db.session.add(o)
    db.session.commit()