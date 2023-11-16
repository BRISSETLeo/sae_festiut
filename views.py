from flask import render_template
from .app import app
from . import models
from flask import request, redirect, url_for

# accueil
@app.route('/')
def accueil():
    return render_template(
        "accueil.html",
        billets = [(0,"Nom du billet", "Description du billet admettons le texte est un peu trop grand pour cette page à quel moment je pourrais voir si c'est goodDescription du billet admettons le texte est un peu trop grand pour cette page à quel moment je pourrais voir si c'est goodDescription du billet admettons le texte est un peu trop grand pour cette page à quel moment je pourrais voir si c'est goodDescription du billet admettons le texte est un peu trop grand pour cette page à quel moment je pourrais voir si c'est goodDescription du billet admettons le texte est un peu trop grand pour cette page à quel moment je pourrais voir si c'est goodDescription du billet admettons le texte est un peu trop grand pour cette page à quel moment je pourrais voir si c'est goodDescription du billet admettons le texte est un peu trop grand pour cette page à quel moment je pourrais voir si c'est goodDescription du billet admettons le texte est un peu trop grand pour cette page à quel moment je pourrais voir si c'est goodDescription du billet admettons le texte est un peu trop grand pour cette page à quel moment je pourrais voir si c'est good ou non ?", "18/03/2024", "Saint Jacques le moine", "$50000"),(1,"Nom du billet2", "Description du billet2", "18/03/2025", "Saint Jacques le moine2", "$100")]
    )

@app.route('/connexion')
def connexion():
    return render_template(
        "connexion.html"
    )

@app.route('/inscription')
def inscription():
    return render_template(
        "inscription.html"
    )

@app.route('/save_inscription', methods=("POST",))
def save_inscription():
    nom = request.form['nom']
    tel = request.form['tel']
    email = request.form['email']
    mdp = request.form['mdp']
    cursor = models.get_cursor()
    models.save_inscription(nom, tel, email, mdp)
    models.close_cursor(cursor)
    return redirect(url_for('accueil'))