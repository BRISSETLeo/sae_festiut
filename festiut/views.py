import base64
from markupsafe import Markup
from .app import app, login_manager
from flask import render_template,request, redirect, url_for
from .models import Utilisateur, save_user, Festival, db, TypeEvent, Event
from hashlib import sha256
from flask_login import login_user, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from datetime import datetime, timedelta
from itertools import combinations
from sqlalchemy.sql.expression import func

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
    festival = Festival.query.first()
    events = Event.query.order_by(func.random()).limit(3).all()
    return render_template("home.html", festival=festival, events=events)

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

@app.route("/billeterie/")
def billeterie():
    billets = Billet.query.all()
    return render_template("billeterie.html",
                           billets=billets)

@app.template_filter('str')
def string_filter(value):
    return str(value)

@app.route("/info_billet/<int:idBillet>") 
def info_billet(idBillet):
    billet = Billet.query.filter_by(idBillet=idBillet).first()
    festival = Festival.query.first()
    
    jours_disponibles = [festival.dateDebut + timedelta(n) for n in range((festival.dateFin - festival.dateDebut).days + 1)]

    jours_disponibles_formates = [date.strftime('%A %d %B') for date in jours_disponibles]

    combinaisons_jours = list(combinations(jours_disponibles_formates, 2))
    combinaisons_successives = [comb for comb in combinaisons_jours if jours_disponibles_formates.index(comb[0]) == jours_disponibles_formates.index(comb[1]) - 1]

    return render_template("info_billet.html",
                           billet=billet, jours_disponibles=jours_disponibles_formates, duo_disponible=combinaisons_successives)

@app.route("/programme")
def programme():
    events = Event.query.all()
    return render_template("programme.html", events=events)
    
@app.route("/acheter_billet/<int:idBillet>", methods =("GET","POST" ,))
def acheter_billet(idBillet):
    billet = Billet.query.filter_by(idBillet=idBillet).first()
    festival = Festival.query.first()
    if request.method == "POST":
        if current_user.is_authenticated:
            utilisateur_nom = current_user.nom
        else:
            return redirect(url_for('login'))
        
        if billet.nomTypeBillet == 'Journée':
            dateDebut = request.form['dateDebut']
            dateFin = dateDebut

        elif billet.nomTypeBillet == 'Totalité du festival':
            dateDebut = festival.dateDebut
            dateFin = festival.dateFin

        elif billet.nomTypeBillet == '2 jours':
            dateDebut_str = request.form['dateDebut'][2:12]
            dateDebut = datetime.strptime(dateDebut_str, '%Y-%m-%d')
            dateFin = dateDebut + timedelta(days=1)

        for _ in range(int(request.form['quantite'])):
            BilletAchete.acheter_billet(idBillet, utilisateur_nom, dateDebut, dateFin)

        return redirect(url_for('home'))
    return render_template("acheter_billet.html", billet=billet)
    
@app.route("/admin/ajouter_evenement/")
def ajouter_evenement():
    types_events = TypeEvent.query.all()
    jours_disponibles = les_jours_disponibles(Festival.query.first())
    return render_template("ajouter_evenement.html", types=types_events, jours_disponibles=jours_disponibles)

@app.route('/admin/add_evenement/', methods=['POST'])
def add_evenement():
    nomEvent = request.form.get('nomEvent')
    typeEvent = request.form.get('typeEvent')
    dateDebut_str = request.form.get('dateDebut')
    dateFin_str = request.form.get('dateFin')
    nomLieu = request.form.get('nomLieu')
    descriptionEvent = request.form.get('descriptionEvent')
    imageEvent = request.files.get('image')
    
    dateDebut = datetime.strptime(dateDebut_str, '%Y-%m-%dT%H:%M')
    dateFin = datetime.strptime(dateFin_str, '%Y-%m-%dT%H:%M')
    
    festival = Festival.query.first()
    dateDebFestival = festival.dateDebut
    dateFinFestival = festival.dateFin 

    Event.enregistrer_nouvel_event(nom_event=nomEvent, type_event=typeEvent, date_debut=dateDebut, date_fin=dateFin, nom_lieu=nomLieu, description_event=descriptionEvent, image_event=imageEvent.read())

    return redirect(url_for('home'))

@app.template_filter('byte_to_image')
def byte_to_image(byte):
    image_base64 = base64.b64encode(byte).decode('utf-8')
    return Markup(f'<img src="data:image/png;base64,{image_base64}" alt="Image">')
    
def les_jours_disponibles(festival):
    return [date.strftime('%Y-%m-%d') for date in 
                     (festival.dateDebut + timedelta(n) for n in range((festival.dateFin - festival.dateDebut).days + 1))]