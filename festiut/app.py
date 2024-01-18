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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ozocak:ozocak@servinfo-maria:3306/DBozocak'

db = SQLAlchemy(app)

# from .models import Role, Festival, Billet
# with app.app_context():
#     print("Deleting database tables...")
#     db.drop_all()
#     print("Creating database tables...")
#     db.create_all()
    
#     if Role.query.count() == 0:    
#         utilisateur = Role(nomRole="Utilisateur")
#         administrateur = Role(nomRole="Administrateur")
#         db.session.add(utilisateur)
#         db.session.add(administrateur)

#         festival = Festival(
#             nomFestival="FestIUT'O 2ème édition",
#             dateDebut="2024-05-02 14:00:00",
#             dateFin="2024-08-02 14:00:00",
#             nomLieu="IUT de Lens"
#         )
#         db.session.add(festival)
        
#         imageToBinary = open(mkpath("static/images/billet.png"), "rb").read()

#         billetJournee = Billet(nomTypeBillet="Journée",imageBillet=imageToBinary)
#         billet2Jours = Billet(nomTypeBillet="2 jours")
#         billetTotaliteDuFestival = Billet(nomTypeBillet="Totalité du festival")
#         db.session.add(billetJournee)
#         db.session.add(billet2Jours)
#         db.session.add(billetTotaliteDuFestival)

#         db.session.commit()