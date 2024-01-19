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
    nomFestival = db.Column(db.String(50), primary_key=True, nullable=False)
    villeFestival = db.Column(db.String(50), nullable=False)
    codePostalFestival = db.Column(db.String(5), nullable=False)
    dateDebutFestival = db.Column(db.Date, nullable=False)

    journeesFestival = db.relationship('Journee', backref='festival', lazy=True)

    def __repr__(self):
        return f"<Festival {self.nomFestival}: {self.ville} {self.codePostal}>"

class Lieu(db.Model):
    nomLieu = db.Column(db.String(50), primary_key=True, nullable=False)
    adresseLieu = db.Column(db.String(50), nullable=False)
    nbPlaceLieu = db.Column(db.Integer, nullable=False)

    journeesLieu = db.relationship('Journee', backref='lieu', lazy=True)
    eventsLieu = db.relationship('Event', backref='lieu', lazy=True)
    
    def __repr__(self):
        return f"<Lieu {self.nomLieu}: {self.adresse} {self.ville} {self.codePostal}>"

class Journee(db.Model):
    idJournee = db.Column(db.Integer, primary_key=True, nullable=False)
    nomFestivalJournee = db.Column(db.String(50), db.ForeignKey('festival.nomFestival'), nullable=False)
    dateJournee = db.Column(db.Date, nullable=False)
    lieuJournee = db.Column(db.String(50), db.ForeignKey('lieu.nomLieu'), nullable=False)
    
    eventsJournee = db.relationship('Event', backref='journee', lazy=True)

    def __repr__(self):
        return f"<Journee {self.idJournee}: {self.date} {self.idFestival}>"

class TypeEvent(db.Model):
    nomTypeEvent = db.Column(db.String(50), primary_key=True, nullable=False)

    def __repr__(self):
        return f"<TypeEvent {self.nomEvent}>"

class Event(db.Model):
    idEvent = db.Column(db.Integer, primary_key=True, nullable=False)
    nomEvent = db.Column(db.String(50), nullable=False)
    typeEvent = db.Column(db.String(50), db.ForeignKey('type_event.nomTypeEvent'), nullable=False)
    lieuEvent = db.Column(db.String(50), db.ForeignKey('lieu.nomLieu'), nullable=False)
    descriptionEvent = db.Column(db.String(500), nullable=False)
    imageEventEvent = db.Column(db.LargeBinary(length=(2**32)-1), nullable=True)
    estGratuit = db.Column(db.Boolean, nullable=False)

    journeeEvent = db.Column(db.Integer, db.ForeignKey('journee.idJournee'), nullable=False)

    def __repr__(self):
        return f"<Event {self.nomEvent}: {self.descriptionEvent}>"

@login_manager.user_loader
def load_user(nom):
    return Utilisateur.query.get(nom)

def save_user(user):
    db.session.add(user)
    db.session.commit()


### REQUETES SQL ###