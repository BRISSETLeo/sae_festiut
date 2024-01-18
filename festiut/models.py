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
    nomLieu = db.Column(db.String(25), nullable=False)
    imageBanner = db.Column(db.LargeBinary, nullable=True)
    
    # Relation avec BilletFestival
    billets = db.relationship('BilletFestival', back_populates='festival')
    
    def __repr__(self):
        return f"<Festival {self.nomFestival}: {self.dateDebut} {self.dateFin} {self.nomLieu}>"

class Billet(db.Model):
    idBillet = db.Column(db.Integer, primary_key=True, nullable=False)
    nomTypeBillet = db.Column(db.String(25), nullable=False)
    
    # Relation avec BilletAchete
    billets_achetes = db.relationship('BilletAchete', back_populates='billet')
    
    def __repr__(self):
        return f"<Billet {self.idBillet}: {self.nomTypeBillet}"

class BilletFestival(db.Model):
    idFestival = db.Column(db.Integer, db.ForeignKey('festival.idFestival'), primary_key=True, nullable=False)
    idBillet = db.Column(db.Integer, db.ForeignKey('billet.idBillet'), primary_key=True, nullable=False)
    prix = db.Column(db.Float, nullable=False)
    
    # Relation avec Festival
    festival = db.relationship('Festival', back_populates='billets')
    
    def __repr__(self):
        return f"<BilletFestival {self.idFestival}: {self.idBillet}"

class BilletAchete(db.Model):
    idBilletAchete = db.Column(db.Integer,db.ForeignKey('billet.idBillet'), primary_key=True, nullable=False)
    
    dateDebut = db.Column(db.DateTime, nullable=False)
    dateFin = db.Column(db.DateTime, nullable=False)
    
    # Relation avec Billet
    billet = db.relationship('Billet', back_populates='billets_achetes')

    def __repr__(self):
        return f"<BilletAchete {self.idBilletAchete}: {self.dateDebut} {self.dateFin}"

@login_manager.user_loader
def load_user(nom):
    return Utilisateur.query.get(nom)

def save_user(user):
    db.session.add(user)
    db.session.commit()
