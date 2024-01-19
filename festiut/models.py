from .app import db, login_manager
from flask_login import UserMixin
import datetime

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

    def enregistrer_nouveau_lieu(nomLieu, adresseLieu, nbPlaceLieu):
        lieu = Lieu(nomLieu=nomLieu, adresseLieu=adresseLieu, nbPlaceLieu=nbPlaceLieu)
        db.session.add(lieu)
        db.session.commit()
    
    def __repr__(self):
        return f"<Lieu {self.nomLieu}: {self.adresse} {self.ville} {self.codePostal}>"

class Journee(db.Model):
    idJournee = db.Column(db.Integer, primary_key=True, nullable=False)
    nomFestivalJournee = db.Column(db.String(50), db.ForeignKey('festival.nomFestival'), nullable=False)
    dateJournee = db.Column(db.Date, nullable=False)
    lieuJournee = db.Column(db.String(50), db.ForeignKey('lieu.nomLieu'), nullable=False)
    
    eventsJournee = db.relationship('Event', backref='journee', lazy=True)

    def enregistrer_nouvelle_journee(nomJournee, lieuJournee, date_debut):
        journee = Journee(
            nomFestivalJournee=nomJournee,
            dateJournee=date_debut,
            lieuJournee=lieuJournee
        )
        db.session.add(journee)
        db.session.commit()

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
    heureDebutEvent = db.Column(db.Time, nullable=False)
    heureFinEvent = db.Column(db.Time, nullable=False)
    descriptionEvent = db.Column(db.String(500), nullable=False)
    imageEvent = db.Column(db.LargeBinary(length=(2**32)-1), nullable=True)
    estGratuit = db.Column(db.Boolean, nullable=False)

    journeeEvent = db.Column(db.Integer, db.ForeignKey('journee.idJournee'), nullable=False)

    def enregistrer_nouvel_event(nomEvent, typeEvent, lieuEvent, heureDebutEvent, heureFinEvent, descriptionEvent, imageEvent, estGratuit, journeeEvent):
        event = Event(nomEvent=nomEvent, typeEvent=typeEvent, lieuEvent=lieuEvent, heureDebutEvent=heureDebutEvent, heureFinEvent=heureFinEvent, descriptionEvent=descriptionEvent, imageEvent=imageEvent, estGratuit=estGratuit, journeeEvent=journeeEvent)
        db.session.add(event)
        db.session.commit()

    def __repr__(self):
        return f"<Event {self.nomEvent}: {self.descriptionEvent}>"

class Groupe(db.Model):
    nomGroupe = db.Column(db.String(50), primary_key=True, nullable=False)
    styleGroupe = db.Column(db.String(50), nullable=False)
    imageGroupe = db.Column(db.LargeBinary(length=(2**32)-1), nullable=True)

    artistesGroupe = db.relationship('Artiste', backref='groupe', lazy=True)

    def __repr__(self):
        return f"<Groupe {self.nomGroupe}: {self.styleGroupe}>"

class Artiste(db.Model):
    nomArtiste = db.Column(db.String(50), primary_key=True, nullable=False)
    nomGroupeArtiste = db.Column(db.String(50), db.ForeignKey('groupe.nomGroupe'), nullable=True)
    styleArtiste = db.Column(db.String(50), nullable=False)
    imageArtiste = db.Column(db.LargeBinary(length=(2**32)-1), nullable=True)

    def __repr__(self):
        return f"<Artiste {self.nomArtiste}: {self.styleArtiste}>"

class Logement(db.Model):
    idLogement = db.Column(db.Integer, primary_key=True, nullable=False)
    nomLogement = db.Column(db.String(50), nullable=False)
    adresseLogement = db.Column(db.String(50), nullable=False)
    codePostalLogement = db.Column(db.String(5), nullable=False)
    villeLogement = db.Column(db.String(50), nullable=False)
    nbPlaceLogement = db.Column(db.Integer, nullable=False)
    prixLogement = db.Column(db.Integer, nullable=False)
    descriptionLogement = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"<Logement {self.nomLogement}: {self.adresseLogement} {self.codePostalLogement} {self.villeLogement}>"

class ParticiperGroupe(db.Model):
    nomGroupe = db.Column(db.String(50), db.ForeignKey('groupe.nomGroupe'), primary_key=True, nullable=False)
    idEvent = db.Column(db.Integer, db.ForeignKey('event.idEvent'), unique=True, primary_key=True, nullable=False)
    idLogement = db.Column(db.Integer, db.ForeignKey('logement.idLogement'), nullable=True)

    def __repr__(self):
        return f"<ParticiperGroupe {self.nomGroupe}: {self.idEvent}>"

class ParticiperArtiste(db.Model):
    nomArtiste = db.Column(db.String(50), db.ForeignKey('artiste.nomArtiste'), primary_key=True, nullable=False)
    idEvent = db.Column(db.Integer, db.ForeignKey('event.idEvent'), unique=True, primary_key=True, nullable=False)
    idLogement = db.Column(db.Integer, db.ForeignKey('logement.idLogement'), nullable=True)

    def __repr__(self):
        return f"<ParticiperArtiste {self.nomArtiste}: {self.idEvent}>"
    
class TypeLien(db.Model):
    nomTypeLien = db.Column(db.String(50), primary_key=True, nullable=False)

    def __repr__(self):
        return f"<TypeLien {self.nomTypeLien}>"

class Lien(db.Model):
    idLien = db.Column(db.Integer, primary_key=True, nullable=False)
    typeLien = db.Column(db.String(50), db.ForeignKey('type_lien.nomTypeLien'), nullable=False)
    urlLien = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Lien {self.typeLien}: {self.urlLien}>"
    
class LienGroupe(db.Model):
    nomGroupe = db.Column(db.String(50), db.ForeignKey('groupe.nomGroupe'), primary_key=True, nullable=False)
    idLien = db.Column(db.Integer, db.ForeignKey('lien.idLien'), unique=True, primary_key=True, nullable=False)
    dateLien = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<LienGroupe {self.nomGroupe}: {self.idLien}>"

class LienArtiste(db.Model):
    nomArtiste = db.Column(db.String(50), db.ForeignKey('artiste.nomArtiste'), primary_key=True, nullable=False)
    idLien = db.Column(db.Integer, db.ForeignKey('lien.idLien'), unique=True, primary_key=True, nullable=False)
    dateLien = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<LienArtiste {self.nomArtiste}: {self.idLien}>"

@login_manager.user_loader
def load_user(nom):
    return Utilisateur.query.get(nom)

def save_user(user):
    db.session.add(user)
    db.session.commit()


### REQUETES SQL ###