import click
from .app import app , db

@app.cli. command()
def loaddb():
    db.create_all()
    
    from .models import Utilisateur
    
    auteur = Utilisateur(nom="Pierre", prenom="Paul")
    db.session.add(auteur)
    db.session.commit()
    