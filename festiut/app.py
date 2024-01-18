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

from .models import Role, Festival, Billet, BilletFestival
with app.app_context():
    print("Deleting database tables...")
    db.drop_all()
    print("Creating database tables...")
    db.create_all()
    
    if Role.query.count() == 0:    
        utilisateur = Role(nomRole="Utilisateur")
        administrateur = Role(nomRole="Administrateur")
        db.session.add(utilisateur)
        db.session.add(administrateur)

        festival = Festival(
            nomFestival="FestIUT'O 2ème édition",
            dateDebut="2024-05-02 14:00:00",
            dateFin="2024-08-02 14:00:00",
            nomLieu="IUT de Lens"
        )
        db.session.add(festival)

        billetJournee = Billet(nomTypeBillet="Journée")
        billet2Jours = Billet(nomTypeBillet="2 jours")
        billetTotaliteDuFestival = Billet(nomTypeBillet="Totalité du festival")
        db.session.add(billetJournee)
        db.session.add(billet2Jours)
        db.session.add(billetTotaliteDuFestival)

        db.session.commit()

        billetJourneFestival = BilletFestival(
            idFestival=festival.idFestival,
            idBillet=billetJournee.idBillet,
            prix=45
        )
        billet2JourFestival = BilletFestival(
            idFestival=festival.idFestival,
            idBillet=billet2Jours.idBillet,
            prix=80
        )
        billetTotaliteFestival = BilletFestival(
            idFestival=festival.idFestival,
            idBillet=billetTotaliteDuFestival.idBillet,
            prix=140
        )

        db.session.add(billetJourneFestival)
        db.session.add(billet2JourFestival)
        db.session.add(billetTotaliteFestival)
        db.session.commit()

    
# from . models import User
# from hashlib import sha256
# m = sha256 ()
# m. update( password .encode ())
# u = User( username =username , password =m. hexdigest ())
# db. session .add(u)
# db. session .commit ()