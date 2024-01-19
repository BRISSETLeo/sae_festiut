from festiut.models import Journee
from .app import app , db

@app.cli. command()
def loaddb():
    print("Deleting database tables...")
    db.drop_all()
    print("Creating database tables...")
    db.create_all()
    
    from .models import Role, Festival, Utilisateur, TypeEvent, TypeLien, StyleMusique, TypeBillet;
        
    db.session.add(Role(nomRole="Utilisateur"))
    db.session.add(Role(nomRole="Administrateur"))
    db.session.commit()
    
    db.session.add(Utilisateur(nom="adm", password="86f65e28a754e1a71b2df9403615a6c436c32c42a75a10d02813961b86f1e428", monRole="Administrateur"))
    
    festival = Festival(
        nomFestival="FestIUT'O 2ème édition",
        villeFestival="Orléans",
        codePostalFestival="45000",
        dateDebutFestival="2024-01-19"
    )
    db.session.add(festival)
        
    billetJournee = TypeBillet(
        nomTypeBillet="Journée",
        prixBillet=49
    )

    billet2Jours = TypeBillet(
        nomTypeBillet="2 jours",
        prixBillet=70
    )

    billetTotaliteDuFestival = TypeBillet(
        nomTypeBillet="Totalité du festival",
        prixBillet=90
    )
    
    db.session.add(TypeEvent(nomTypeEvent="Concert"))
    db.session.add(TypeEvent(nomTypeEvent="Spectacle"))
    db.session.add(TypeEvent(nomTypeEvent="Conférence"))
    db.session.add(TypeEvent(nomTypeEvent="Exposition"))
    db.session.add(TypeEvent(nomTypeEvent="Projection"))
    db.session.add(TypeEvent(nomTypeEvent="Atelier"))
    db.session.add(TypeEvent(nomTypeEvent="Rencontre"))
    db.session.add(TypeEvent(nomTypeEvent="Débat"))
    db.session.add(TypeEvent(nomTypeEvent="Dédicace"))

    db.session.add(TypeLien(nomTypeLien="Vidéo"))
    db.session.add(TypeLien(nomTypeLien="Réseau"))

    db.session.add(StyleMusique(nomStyleMusique="Rock"))
    db.session.add(StyleMusique(nomStyleMusique="Pop"))
    db.session.add(StyleMusique(nomStyleMusique="Rap"))
    db.session.add(StyleMusique(nomStyleMusique="Classique"))
    db.session.add(StyleMusique(nomStyleMusique="Jazz"))
    db.session.add(StyleMusique(nomStyleMusique="Electro"))
    db.session.add(StyleMusique(nomStyleMusique="Reggae"))
    db.session.add(StyleMusique(nomStyleMusique="Country"))
    db.session.add(StyleMusique(nomStyleMusique="Metal"))
    db.session.add(StyleMusique(nomStyleMusique="Variété"))
    db.session.add(StyleMusique(nomStyleMusique="Folk"))

    db.session.commit()    
    
    
    
    