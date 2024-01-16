from .app import app, login_manager
from flask import render_template,request, redirect, url_for
from .models import Utilisateur, save_user
from hashlib import sha256
from flask_login import login_user, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField, PasswordField
from wtforms . validators import DataRequired

class LoginForm(FlaskForm):
    nom = StringField('Nom')
    password = PasswordField('Password')
    def get_authenticated_user(self):
        user = Utilisateur.query.get(self.nom.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.password else None
    
class RegisterForm(FlaskForm):
    nom = StringField('Nom')
    password = PasswordField('Password')
    def get_register_user(self):
        user = Utilisateur.query.get(self.nom.data)
        if user is not None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        user = Utilisateur(nom=self.nom.data, password=passwd, monRole="Utilisateur")
        save_user(user)
        return user

@app.route("/")
def home():
    return render_template("home.html")

@login_manager.user_loader
def load_user(nom):
    return Utilisateur.query.get(nom)

@app.route("/login/", methods =("GET","POST" ,))
def login():
    f = LoginForm ()
    if f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            return redirect(url_for("home"))
    return render_template("login.html", form=f)

@app.route("/register/", methods =("GET","POST" ,))
def register():
    f = RegisterForm()
    if f.validate_on_submit():
        user = f.get_register_user()
        if user:
            login_user(user)
            return redirect(url_for("home"))
    return render_template("register.html", form=f)

@app.route("/logout/")
def logout ():
    logout_user()
    return redirect(url_for('home'))