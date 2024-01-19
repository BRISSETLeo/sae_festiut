from .app import app , db

@app.cli. command()
def loaddb():
    print("Deleting database tables...")
    db.drop_all()
    print("Creating database tables...")
    db.create_all()
    
    from .models import Role, Festival, Utilisateur, TypeEvent;
        
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
        
    # billetJournee = Billet(nomTypeBillet="Journée", imageBillet= open("static/images/Journée.png", "rb").read())
    # billet2Jours = Billet(nomTypeBillet="2 jours", imageBillet= open("static/images/2 jours.png", "rb").read())
    # billetTotaliteDuFestival = Billet(nomTypeBillet="Totalité du festival", imageBillet= open("static/images/Totalité du festival.png", "rb").read())
    # db.session.add(billetJournee)
    # db.session.add(billet2Jours)
    # db.session.add(billetTotaliteDuFestival)
    
    db.session.add(TypeEvent(nomTypeEvent="Concert"))
    db.session.add(TypeEvent(nomTypeEvent="Spectacle"))
    db.session.add(TypeEvent(nomTypeEvent="Conférence"))
    db.session.add(TypeEvent(nomTypeEvent="Exposition"))
    db.session.add(TypeEvent(nomTypeEvent="Projection"))
    db.session.add(TypeEvent(nomTypeEvent="Atelier"))
    db.session.add(TypeEvent(nomTypeEvent="Rencontre"))
    db.session.add(TypeEvent(nomTypeEvent="Débat"))
    db.session.add(TypeEvent(nomTypeEvent="Dédicace"))
    
    db.session.commit()    
    
    
    
    