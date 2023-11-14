from flask import render_template
from .app import app

# accueil
@app.route('/')
def accueil():
    return render_template(
        "accueil.html",
        billets = [(0,"Nom du billet", "Description du billet admettons le texte est un peu trop grand pour cette page à quel moment je pourrais voir si c'est goodDescription du billet admettons le texte est un peu trop grand pour cette page à quel moment je pourrais voir si c'est goodDescription du billet admettons le texte est un peu trop grand pour cette page à quel moment je pourrais voir si c'est goodDescription du billet admettons le texte est un peu trop grand pour cette page à quel moment je pourrais voir si c'est goodDescription du billet admettons le texte est un peu trop grand pour cette page à quel moment je pourrais voir si c'est goodDescription du billet admettons le texte est un peu trop grand pour cette page à quel moment je pourrais voir si c'est goodDescription du billet admettons le texte est un peu trop grand pour cette page à quel moment je pourrais voir si c'est goodDescription du billet admettons le texte est un peu trop grand pour cette page à quel moment je pourrais voir si c'est goodDescription du billet admettons le texte est un peu trop grand pour cette page à quel moment je pourrais voir si c'est good ou non ?", "18/03/2024", "Saint Jacques le moine", "$50000"),(1,"Nom du billet2", "Description du billet2", "18/03/2025", "Saint Jacques le moine2", "$100")]
    )