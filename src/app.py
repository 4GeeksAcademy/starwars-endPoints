"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Personajes, Planetas, Favoritos
import json
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code
# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    user=User.query.all()
    if user == []:
        return jsonify ({"msg":"no existen usuarios"})
    resultado = list(map(lambda usuario:usuario.serialize(),user))
    
    return jsonify(resultado), 200

@app.route('/planetas', methods=['GET'])
def get_planetas():
    planetas=Planetas.query.all()
    if planetas == []:
        return jsonify ({"msg":"no existen planetas"})
    resultado = list(map(lambda planeta:planeta.serialize(),planetas))
    
    return jsonify(resultado), 200

@app.route('/planetas/<int:id>', methods=['GET'])
def get_planeta_id(id):
    planeta=Planetas.query.filter_by(id=id).first()
    if planeta is None:
        return jsonify ({"msg":"no existen planetas"})
    return jsonify(planeta.serialize()), 200


@app.route('/people', methods=['GET'])
def get_People():
    personajes=Personajes.query.all()
    if personajes == []:
        return jsonify ({"msg":"no existen personajes"})
    resultado = list(map(lambda personaje:personaje.serialize(),personajes))
    
    return jsonify(resultado), 200

@app.route('/people/<int:id>', methods=['GET'])
def get_people_id(id):
    people=Personajes.query.filter_by(id=id).first()
    if people is None:
        return jsonify ({"msg":"no existen personajes"})
    return jsonify(people.serialize()), 200


@app.route('/favorite/people/<int:people_id>', methods=['POST',"DELETE"])
def post_people_id(people_id):
    body = json.loads(request.data)
    usuario=body['user_id']

    userexist=User.query.filter_by(id=usuario).first()
    if userexist is None:  
        return jsonify ({"msg":"no existe el usuario"})
    
    peopleexist=Personajes.query.filter_by(id=people_id).first()
    if peopleexist is None:  
        return jsonify ({"msg":"no existe el personaje"})
    
    if request.method=="POST":
        nuevoFavorito=Favoritos(
            userid=usuario,
            personajesid=people_id

    )
        db.session.add(nuevoFavorito)
        db.session.commit()
        return jsonify ({"msg":"favorito creado"})
    

    if request.method=="DELETE":
        personaje=Favoritos.query.filter_by(personajesid=people_id).first()
        db.session.delete(personaje)
        db.session.commit()
        return jsonify ({"msg":"favorito eliminado"})
    
@app.route('/favorite/planets/<int:planet_id>', methods=['POST',"DELETE"])
def post_planet_id(planet_id):
    body = json.loads(request.data)
    usuario=body['user_id']

    userexist=User.query.filter_by(id=usuario).first()
    if userexist is None:  
        return jsonify ({"msg":"no existe el usuario"})
    
    planetexist=Planetas.query.filter_by(id=planet_id).first()
    if planetexist is None:  
        return jsonify ({"msg":"no existe el planeta"})
    
    if request.method=="POST":
        nuevoFavorito=Favoritos(
            userid=usuario,
            planetasid=planet_id

    )
        db.session.add(nuevoFavorito)
        db.session.commit()
        return jsonify ({"msg":"favorito creado"})
    

    if request.method=="DELETE":
        planeta=Favoritos.query.filter_by(planetasid=planet_id).first()
        db.session.delete(planeta)
        db.session.commit()
        return jsonify ({"msg":"favorito eliminado"})

@app.route('/favorite/user/<int:id>', methods=['GET'])
def get_favoritos_id(id):
    people=Favoritos.query.filter_by(userid=id).all()
    if people == []:
        return jsonify ({"msg":"no existen favoritos"})
    resultado = list(map(lambda personaje:personaje.serialize(),people))
    
    return jsonify(resultado), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
