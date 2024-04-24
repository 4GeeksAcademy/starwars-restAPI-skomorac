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
from models import db, People, Planets, User
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
@app.route('/planets', methods=['GET'])
@app.route('/people', methods=['GET'])

def get_all_items():
    if request.path == '/people':
        items = People.query.all()
    elif request.path == '/planets':
        items = Planets.query.all()
    elif request.path == '/user':
        items = User.query.all()

    serialized_items = [item.serialize() for item in items]
    return jsonify(serialized_items), 200

@app.route('/<model>/<int:item_id>', methods=['GET'])
def get_item(model, item_id):
    if model == 'people':
        item = People.query.get(item_id)
    elif model == 'planets':
        item = Planets.query.get(item_id)
    elif model == 'user':
        item = User.query.get(item_id)
    else:
        return jsonify({"error": "Invalid model name"}), 400
    
    if item is None:
        return jsonify({"error": f"{model.capitalize()} with id {item_id} doesn't exist"}), 404

    serialized_item = item.serialize()
    return jsonify(serialized_item), 200


@app.route('/people', methods=['POST'])
def create_person():

    new_person = request.get_json()

    if 'name' not in new_person:
        return "Name cannot be empty", 400
    

    new_person = People(
        name = new_person['name'], 
        height = new_person['height'],
        mass = new_person['mass'],
        hair_color = new_person['hair_color'],
        skin_color = new_person['skin_color'],
        eye_color = new_person['eye_color'],
        birth_year = new_person['birth_year'],
        gender = new_person['gender'],
        homeworld = new_person['homeworld'],
    )

    db.session.add(new_person)
    db.session.commit()

    return jsonify({"msg": "New Person is created"}), 201


@app.route('/planets', methods=['POST'])
def create_planet():

    new_planet = request.get_json()

    if 'name' not in new_planet:
        return "Name cannot be empty", 400
    

    new_planet = Planets(
        name = new_planet['name'], 
        diameter = new_planet['diameter'],
        rotation_period = new_planet['rotation_period'],
        orbital_period = new_planet['orbital_period'],
        gravity = new_planet['gravity'],
        population = new_planet['population'],
        climate = new_planet['climate'],
        terrain = new_planet['terrain'],
    )

    db.session.add(new_planet)
    db.session.commit()

    return jsonify({"msg": "New Planet is created"}), 201


@app.route('/user', methods=['POST'])
def create_user():

    new_user = request.get_json()

    if 'name' not in new_user:
        return "Name cannot be empty", 400
    

    new_user = User(
        name = new_user['name'], 
        age = new_user['age'],
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "New User is created"}), 201



@app.route('/people/<int:person_id>', methods=['PUT'])
def update_person(person_id):
    
    updated_person = request.get_json()
    old_person = People.query.get(person_id)

    if old_person is None:
        return "Person with id: " + str(person_id) + " doesn't exist", 400 
    
    if 'name' in updated_person:
        old_person.name = updated_person['name']

    if 'birth_year' in updated_person:
        old_person.birth_year = updated_person['birth_year']

    if 'eye_color' in updated_person:
        old_person.eye_color = updated_person['eye_color']

    if 'gender' in updated_person:
        old_person.gender = updated_person['gender']

    if 'hair_color' in updated_person:
        old_person.hair_color = updated_person['hair_color']

    if 'height' in updated_person:
        old_person.height = updated_person['height']

    if 'homeworld' in updated_person:
        old_person.homeworld = updated_person['homeworld']

    if 'mass' in updated_person:
        old_person.mass = updated_person['mass']

    if 'skin_color' in updated_person:
        old_person.skin_color = updated_person['skin_color']

    db.session.commit()

    return jsonify({"msg": "Person is updated"}), 200


@app.route('/planets/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    updated_planet = request.get_json()
    old_planet = Planets.query.get(planet_id)

    if old_planet is None:
        return "Planet with id: " + str(planet_id) + " doesn't exist", 400 
    
    if 'name' in updated_planet:
        old_planet.name = updated_planet['name']

    if 'diameter' in updated_planet:
        old_planet.diameter = updated_planet['diameter']

    if 'rotation_period' in updated_planet:
        old_planet.rotation_period = updated_planet['rotation_period']

    if 'orbital_period' in updated_planet:
        old_planet.orbital_period = updated_planet['orbital_period']

    if 'gravity' in updated_planet:
        old_planet.gravity = updated_planet['gravity']

    if 'population' in updated_planet:
        old_planet.population = updated_planet['population']

    if 'climate' in updated_planet:
        old_planet.climate = updated_planet['climate']

    if 'terrain' in updated_planet:
        old_planet.terrain = updated_planet['terrain']

    db.session.commit()

    return jsonify({"msg": "Planet is updated"}), 200


@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    updated_user = request.get_json()
    old_user = User.query.get(user_id)

    if old_user is None:
        return "User with id: " + str(user_id) + " doesn't exist", 400 
    
    if 'name' in updated_user:
        old_user.name = updated_user['name']

    if 'age' in updated_user:
        old_user.age = updated_user['age']

    db.session.commit()

    return jsonify({"msg": "User is updated"}), 200



@app.route('/<model>/<int:item_id>', methods=['DELETE'])
def delete_item(model, item_id):
    if model == 'people':
        item_to_delete = People.query.get(item_id)
    elif model == 'planets':
        item_to_delete = Planets.query.get(item_id)
    else:
        return jsonify({"error": "Invalid model name"}), 400

    if item_to_delete is None:
        return jsonify({"error": f"{model.capitalize()} with id {item_id} doesn't exist"}), 404
    
    db.session.delete(item_to_delete)
    db.session.commit()

    return jsonify({"msg": f"{model.capitalize()} is deleted"}), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
