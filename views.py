from .app import app, db
from flask import render_template, url_for, redirect, request
from .models import Compte, Role
from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField, PasswordField
from wtforms.validators import DataRequired
from hashlib import sha256
from flask_login import login_user, current_user, login_required, logout_user
from flask import request

@app.route("/")
def home():
    return render_template("accueil.html")

class AuthorForm(FlaskForm):
    pseudo = HiddenField('pseudo')
    name = StringField('Nom', validators=[DataRequired()]) 

class LoginForm(FlaskForm):
    pseudo = StringField('pseudo')
    password = PasswordField('Password')
    next = HiddenField()

    def get_authenticated_user(self):
        compte = Compte.query.get(self.pseudo.data) 
        if compte is None:
            return None
        
        # Hashage
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()

        return compte if passwd == compte.password else None

@app.route("/login/", methods=["GET", "POST" ,])
def login():
    f = LoginForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        compte = Compte.query.get(f.pseudo.data) 
        if compte:
            login_user(compte)
            return redirect(url_for("home"))
    return render_template("login.html",form=f)

@app.route("/register/", methods=["GET", "POST"])
def register():
    f = LoginForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        compte = Compte.query.get(f.pseudo.data) 
        if compte:
            f.next.data = request.args.get("hidden")
            print("L'utilisateur existe déjà.", "error")
        else:
            m = sha256()
            m.update(f.password.data.encode())
            passwd = m.hexdigest()
            compte = Compte(pseudo=f.pseudo.data, password=passwd)
            db.session.add(compte)
            db.session.commit()
            login_user(compte)
            return redirect(url_for("home"))
    return render_template("login.html", form=f)

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("home"))
