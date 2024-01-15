from .app import app, db, login_manager
from flask_login import UserMixin

class Role(db.Model):
    role = db.Column(db.String(50), primary_key =True)
    
    def __repr__(self):
        """ Redéfinit l'équivalent du toString en java """
        return f"{self.role}"
    
class Compte(db.Model, UserMixin):
    pseudo = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(64))
    role = db.Column(db.String(50), db.ForeignKey("role.role"))
    
    def __repr__(self):
        return f"{self.pseudo} {self.role}"

@login_manager.user_loader
def load_user(username):
    return Compte.query.get(username)