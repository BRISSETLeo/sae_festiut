import base64
from markupsafe import Markup
from .app import app, login_manager
from flask import render_template,request, redirect, url_for
from .models import *
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

@app.route("/admin/ajouter_lieu/")
def ajouter_lieu():
    return render_template("ajouter_lieu.html")

@app.route('/admin/add_lieu/', methods=['POST'])
def add_lieu():
    nomLieu = request.form.get('nomLieu')
    adresseLieu = request.form.get('adresseLieu')
    nbPlaceLieu = request.form.get('nbPlaceLieu')
    
    Lieu.enregistrer_nouveau_lieu(nomLieu=nomLieu, adresseLieu=adresseLieu, nbPlaceLieu=nbPlaceLieu)

    return redirect(url_for('home'))

@app.route("/admin/voir_les_lieux/")
def voir_les_lieux():
    lieux = Lieu.query.all()
    return render_template("voir_les_lieux.html", lieux=lieux)

@app.route("/admin/ajouter_event/")
def ajouter_event():
    types_events = TypeEvent.query.all()
    lieux = Lieu.query.filter(Lieu.journeesLieu.any()).all()
    journees = Journee.query.all()
    return render_template("ajouter_event.html", types=types_events, lieux=lieux, journees=journees)

@app.route('/admin/add_event/', methods=['POST'])
def add_event():
    nomEvent = request.form.get('nomEvent')
    typeEvent = request.form.get('typeEvent')
    lieuEvent = request.form.get('lieuEvent')
    heureDebutEvent = request.form.get('heureDebutEvent')
    heureFinEvent = request.form.get('heureFinEvent')
    descriptionEvent = request.form.get('descriptionEvent')
    imageEvent = request.files.get('image')
    estGratuit = request.form.get('estGratuit')
    journeeEvent = Journee.query.filter_by(lieuJournee=lieuEvent).first()
    
    if(journeeEvent == None):
        return redirect(url_for('ajouter_event'))

    byte = None
    if imageEvent:
        byte = imageEvent.read()
    
    Event.enregistrer_nouvel_event(nomEvent=nomEvent, typeEvent=typeEvent, lieuEvent=lieuEvent, heureDebutEvent=heureDebutEvent, heureFinEvent=heureFinEvent, descriptionEvent=descriptionEvent, imageEvent=byte, estGratuit=estGratuit, journeeEvent=journeeEvent)

    return redirect(url_for('home'))

@app.route("/admin/voir_tous_les_evenements/")
def voir_tous_les_evenements():
    events = Event.query.all()
    return render_template("voir_tous_les_evenements.html", events=events)

@app.route('/admin/ajouter_journee/')
def ajouter_journee():
    lieux = Lieu.query.all()
    festival = Festival.query.first()
    journee = Journee.query.order_by(Journee.idJournee.desc()).first()
    if journee is None:
        journee = festival.dateDebutFestival
    else:
        journee = journee.dateJournee + timedelta(days=1)
    return render_template("ajouter_journee.html", lieux=lieux, journee=journee)

@app.route('/admin/add_journee/', methods=['POST'])
def add_journee():
    lieuJournee = request.form.get('lieu')
    date_debut = request.form.get('date')

    Journee.enregistrer_nouvelle_journee(nomJournee=Festival.query.first().nomFestival, date_debut=date_debut, lieuJournee=lieuJournee)

    return redirect(url_for('home'))

@app.route("/admin/ajouter_artiste/")
def ajouter_artiste():
    groupes = Groupe.query.all()
    styles = StyleMusique.query.all()
    return render_template("ajouter_artiste.html", groupes=groupes, styles=styles)

@app.route('/admin/add_artiste/', methods=['POST'])
def add_artiste():
    nomArtiste = request.form.get('nomArtiste')
    groupeArtiste = request.form.get('groupeArtiste')
    styleArtiste = request.form.get('styleArtiste')
    imageArtiste = request.files.get('imageArtiste')
    
    byte = None
    if imageArtiste:
        byte = imageArtiste.read()

    Artiste.enregistrer_nouvel_artiste(nomArtiste=nomArtiste, groupeArtiste=groupeArtiste, styleArtiste=styleArtiste, imageArtiste=byte)

    return redirect(url_for('home'))

@app.route("/admin/voir_toutes_les_journees/")
def voir_toutes_les_journees():
    journees = Journee.query.all()
    return render_template("voir_toutes_les_journees.html", journees=journees)

@app.route("/admin/voir_tous_les_artistes/")
def voir_tous_les_artistes():
    artistes = Artiste.query.all()
    return render_template("voir_tous_les_artistes.html", artistes=artistes)

@app.route("/admin/ajouter_groupe/")
def ajouter_groupe():
    styles = StyleMusique.query.all()
    artiste = Artiste.query.all()
    return render_template("ajouter_groupe.html", styles=styles, artiste=artiste)

@app.route('/admin/add_groupe/', methods=['POST'])
def add_groupe():
    nomGroupe = request.form.get('nomGroupe')
    styleGroupe = request.form.get('styleGroupe')
    imageGroupe = request.files.get('imageGroupe')
    
    byte = None
    if imageGroupe:
        byte = imageGroupe.read()

    Groupe.enregistrer_nouveau_groupe(nomGroupe=nomGroupe, styleGroupe=styleGroupe, imageGroupe=byte)

    return redirect(url_for('home'))

@app.route("/admin/voir_tous_les_groupes/")
def voir_tous_les_groupes():
    groupes = Groupe.query.all()
    return render_template("voir_les_groupes.html", groupes=groupes)

@app.route("/admin/ajouter_logement/")
def ajouter_logement():
    return render_template("ajouter_logement.html")

@app.route('/admin/add_logement/', methods=['POST'])
def add_logement():
    nomLogement = request.form.get('nomLogement')
    adresseLogement = request.form.get('adresseLogement')
    codePostalLogement = request.form.get('codePostalLogement')
    villeLogement = request.form.get('villeLogement')
    nbPlaceLogement = request.form.get('nbPlaceLogement')
    prixLogement = request.form.get('prixLogement')
    descriptionLogement = request.form.get('descriptionLogement')

    Logement.enregistrer_nouveau_logement(nomLogement=nomLogement, adresseLogement=adresseLogement, codePostalLogement=codePostalLogement, villeLogement=villeLogement, nbPlaceLogement=nbPlaceLogement, prixLogement=prixLogement, descriptionLogement=descriptionLogement)

    return redirect(url_for('home'))

@app.route("/admin/voir_tous_les_logements/")
def voir_tous_les_logements():
    logements = Logement.query.all()
    return render_template("voir_tous_les_logements.html", logements=logements)


def les_jours_disponibles(festival):
    return []
    # return [date.strftime('%Y-%m-%d') for date in 
    #                  (festival.dateDebut + timedelta(n) for n in range((festival.dateFin - festival.dateDebut).days + 1))]