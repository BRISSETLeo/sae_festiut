from flask import render_template
from .app import app
from . import models
from flask import request, redirect, url_for

# accueil
@app.route('/')
def accueil():
    cursor = models.get_cursor()
    billet = models.liste_billets(cursor)
    return render_template(
        "accueil.html",
        billet = billet
    )

@app.route('/connexion')
def connexion():
    utilisateur = models.liste_utilisateurs()
    return render_template(
        "connexion.html",
        utilisateur = utilisateur
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

@app.route('/verif_connexion', methods=("POST",))
def verif_connexion():
    email = request.form['email']
    mdp = request.form['mot_de_passe']
    cursor = models.get_cursor()
    utilisateur = models.verif_connexion(email, mdp)
    models.close_cursor(cursor)
    if utilisateur :
        print("Connexion réussie")
        print(utilisateur)
    else :
        print("Connexion échouée")
    return redirect(url_for('accueil'))
