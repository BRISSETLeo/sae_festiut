from .app import db, login_manager
from flask_login import UserMixin

class Role(db.Model):
    nomRole = db.Column(db.String(25), primary_key=True, nullable=False)
    
    def __repr__(self):
        return f"<Role {self.nom}>"

class Utilisateur(db.Model, UserMixin):
    nom = db.Column(db.String(25), primary_key=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    monRole = db.Column(db.String(25), db.ForeignKey('role.nomRole'), nullable=False)
    
    def get_id(self):
        return self.nom
    
    def __repr__(self):
        return f"<Utilisateur {self.nom}: {self.password} {self.monRole}>"

class Festival(db.Model):
    idFestival = db.Column(db.Integer, primary_key=True, nullable=False)
    nomFestival = db.Column(db.String(25), nullable=False)
    dateDebut = db.Column(db.DateTime, nullable=False)
    dateFin = db.Column(db.DateTime, nullable=False)
    nomVille = db.Column(db.String(25), nullable=False)
    
    def __repr__(self):
        return f"<Festival {self.nomFestival}: {self.dateDebut} {self.dateFin} {self.nomVille}>"

@login_manager.user_loader
def load_user(nom):
    return Utilisateur.query.get(nom)

def save_user(user):
    db.session.add(user)
    db.session.commit()
