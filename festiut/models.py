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
    
    def __repr__(self):
        return f"<Festival {self.nomFestival}: {self.dateDebut} {self.dateFin} {self.nomLieu}>"

class Billet(db.Model):
    idBillet = db.Column(db.Integer, primary_key=True, nullable=False)
    nomTypeBillet = db.Column(db.String(25), nullable=False)
    imageBillet = db.Column(db.LargeBinary, nullable=True)
    
    billets_achetes = db.relationship('BilletAchete', back_populates='billet')
    
    def __repr__(self):
        return f"<Billet {self.idBillet}: {self.nomTypeBillet}"

class BilletAchete(db.Model):
    idBilletAchete = db.Column(db.Integer,db.ForeignKey('billet.idBillet'), primary_key=True, nullable=False)
    
    dateDebut = db.Column(db.DateTime, nullable=False)
    dateFin = db.Column(db.DateTime, nullable=False)
    
    billet = db.relationship('Billet', back_populates='billets_achetes')
    
    def acheter_billet(id_billet, date_debut, date_fin):
        billet_achete = BilletAchete(idBilletAchete=id_billet, dateDebut=date_debut, dateFin=date_fin)
        db.session.add(billet_achete)
        db.session.commit()

    def __repr__(self):
        return f"<BilletAchete {self.idBilletAchete}: {self.dateDebut} {self.dateFin}"
    
class TypeEvent(db.Model):
    nomEvent = db.Column(db.String(25), primary_key=True, nullable=False)
    
    def __repr__(self):
        return f"<TypEvent {self.nomTypEvent}>"
    
class Event(db.Model):
    idEvent = db.Column(db.Integer, primary_key=True, nullable=False)
    nomEvent = db.Column(db.String(25), nullable=False)
    typeEvent = db.Column(db.String(25), db.ForeignKey('type_event.nomEvent'), nullable=False)
    dateDebut = db.Column(db.DateTime, nullable=False)
    dateFin = db.Column(db.DateTime, nullable=False)
    nomLieu = db.Column(db.String(100), nullable=False)
    descriptionEvent = db.Column(db.String(500), nullable=False)
    imageEvent = db.Column(db.LargeBinary, nullable=True)
    
    def enregistrer_nouvel_event(nom_event, type_event, date_debut, date_fin, nom_lieu, description_event, image_event):
        print(image_event)
        event = Event(nomEvent=nom_event, typeEvent=type_event, dateDebut=date_debut, dateFin=date_fin, nomLieu=nom_lieu, descriptionEvent=description_event, imageEvent=image_event)
        db.session.add(event)
        db.session.commit()
    
    def __repr__(self):
        return f"<Event {self.nomEvent}: {self.dateDebut} {self.dateFin} {self.nomLieu}>"

@login_manager.user_loader
def load_user(nom):
    return Utilisateur.query.get(nom)

def save_user(user):
    db.session.add(user)
    db.session.commit()


### REQUETES SQL ###

def get_info_type_billet(idBillet):
    return Billet.query.filter_by(idBillet=idBillet).first()