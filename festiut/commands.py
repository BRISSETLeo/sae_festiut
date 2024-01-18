import click
from .app import app , db

@app.cli. command()
def loaddb():
    print("Deleting database tables...")
    db.drop_all()
    print("Creating database tables...")
    db.create_all()
    
    from .models import Role, Festival, Billet, Utilisateur, TypeEvent;
        
    db.session.add(Role(nomRole="Utilisateur"))
    db.session.add(Role(nomRole="Administrateur"))
    db.session.commit()
    
    db.session.add(Utilisateur(nom="adm", password="86f65e28a754e1a71b2df9403615a6c436c32c42a75a10d02813961b86f1e428", monRole="Administrateur"))
    
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
    
    db.session.add(TypeEvent(nomEvent="Concert"))
    db.session.add(TypeEvent(nomEvent="Spectacle"))
    db.session.add(TypeEvent(nomEvent="Conférence"))
    db.session.add(TypeEvent(nomEvent="Exposition"))
    db.session.add(TypeEvent(nomEvent="Projection"))
    db.session.add(TypeEvent(nomEvent="Atelier"))
    db.session.add(TypeEvent(nomEvent="Rencontre"))
    db.session.add(TypeEvent(nomEvent="Débat"))
    db.session.add(TypeEvent(nomEvent="Dédicace"))
    
    db.session.commit()    
    
    