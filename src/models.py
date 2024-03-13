from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    favoritos = db.relationship("Favoritos")
    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Personajes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20))
    genero = db.Column(db.String(10))
    favoritos = db.relationship("Favoritos")

    def __repr__(self):
        return '<Personajes %r>' % self.nombre
    
    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "genero": self.genero
        }
    
class Planetas (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20))
    habitantes  = db.Column(db.Integer)
    favoritos = db.relationship("Favoritos")

    def __repr__(self):
        return '<Planetas %r>' % self.nombre
    
    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "habitantes": self.habitantes
        }
    
class Favoritos (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid=db.Column(db.Integer,db.ForeignKey("user.id"))
    personajesid=db.Column(db.Integer,db.ForeignKey("personajes.id"))
    planetasid=db.Column(db.Integer,db.ForeignKey("planetas.id"))

    def __repr__(self):
        return '<Favoritos %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "userid": self.userid,
            "personajesid": self.personajesid,
            "planetasid": self.planetasid
        }