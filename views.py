from flask import render_template
from .app import app
from . import models
from flask import request, redirect, url_for

# accueil
@app.route('/')
def accueil():
    utilisateur = models.get_compte()
    festival = models.get_festival()
    return render_template("accueil.html", festival=festival, utilisateur=utilisateur)

@app.route('/connexion')
def connexion():
    utilisateur = models.get_compte()
    return render_template("connexion.html", utilisateur=utilisateur,erreur="")

@app.route('/deconnexion')
def deconnexion():
    models.deconnexion()
    return redirect(url_for('accueil'))

@app.route('/inscription')
def inscription():
    return render_template("inscription.html", utilisateur=None,erreur="")

@app.route('/save_inscription', methods=("POST",))
def save_inscription():
    nom = request.form['nom']
    mdp = request.form['mdp']
    conf_mdp = request.form['conf_mdp']
    if(mdp != conf_mdp):
        return render_template("inscription.html", utilisateur=None, erreur="Les mots de passe ne correspondent pas")
    models.save_inscription(nom, mdp)
    utilisateur = models.get_compte()
    return redirect(url_for('accueil'))

@app.route('/verif_connexion', methods=("POST",))
def verif_connexion():
    pseudo = request.form['pseudo']
    mdp = request.form['mot_de_passe']
    utilisateur = models.verif_connexion(pseudo, mdp)
    if utilisateur is not None:
        return redirect(url_for('accueil'))
    return render_template("connexion.html", utilisateur=None, erreur="Pseudo ou mot de passe incorrecte")
    
@app.route('/nouveau_festival')
def nouveau_festival():
    models.nouveau_festival()
    return redirect(url_for('accueil'))