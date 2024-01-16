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
app.config['SECRET_KEY'] = '1605f5de-4091-48f0-8bcb-b4f98e456835'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ozocak:ozocak@servinfo-maria:3306/DBozocak'

db = SQLAlchemy(app)
with app.app_context():
    print("Creating database tables...")
    if db.create_all():
        from .models import Role
        
        user = Role(nomRole="Utilisateur")
        admin = Role(nomRole="Administrateur")
        db.session.add(user)
        db.session.add(admin)
        db.session.commit()
    
# from . models import User
# from hashlib import sha256
# m = sha256 ()
# m. update( password .encode ())
# u = User( username =username , password =m. hexdigest ())
# db. session .add(u)
# db. session .commit ()