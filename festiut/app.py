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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ozocak:ozocak@servinfo-maria:3306/DBozocak'

db = SQLAlchemy(app)

from .models import Role
with app.app_context():
    print("Creating database tables...")
    db.create_all()
    
    if Role.query.count() == 0:    
        utilisateur = Role(nomRole="Utilisateur")
        administateur = Role(nomRole="Administrateur")
        db.session.add(utilisateur)
        db.session.add(administateur)
        db.session.commit()
    
# from . models import User
# from hashlib import sha256
# m = sha256 ()
# m. update( password .encode ())
# u = User( username =username , password =m. hexdigest ())
# db. session .add(u)
# db. session .commit ()