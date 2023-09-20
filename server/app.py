#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animals')
def list_animals():
    animals = Animal.query.all()
    
    if not animals:
        return make_response('No animals found', 200)
    
    response_body = '<h1>Animals</h1>' + '<ol>'
    for animal in animals:
        response_body += f'<li>Name: {animal.name}, species: {animal.species}</li>'
    response_body += '</ol>'
    
    response = make_response(response_body, 200)
    return response

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()
    
    if not animal:
        response_body = '<h1>404</h1><p>No animal found.</p>'
        response = make_response(response_body, 404)
        return response
    
    response_body = wrap(f'ID: {animal.id}')
    response_body += wrap(f'Name: {animal.name}')
    response_body += wrap(f'Species: {animal.species}')
    response_body += wrap(f'Zookeeper: {animal.zookeeper.name}')
    response_body += wrap(f'Enclosure: {animal.enclosure.environment}')
    response = make_response(response_body, 200)
    return response

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.filter(Zookeeper.id == id).first()
    
    if not zookeeper:
        response_body = '<h1>404</h1><p>No zookeeper found.</p>'
        response = make_response(response_body, 404)
        return response
    
    response_body = wrap(f'ID: {zookeeper.id}')
    response_body += wrap(f'Name: {zookeeper.name}')
    response_body += wrap(f'Birthday: {zookeeper.birthday}')
    
    for animal in zookeeper.animals:
        response_body += wrap(f'Animal: {animal.name}')
    
    response = make_response(response_body, 200)
    return response

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.filter(Enclosure.id == id).first()
    
    if not enclosure:
        response_body = '<h1>404</h1><p>No animal found.</p>'
        response = make_response(response_body, 404)
        return response
    
    response_body = wrap(f'ID: {enclosure.id}')
    response_body += wrap(f'Environment: {enclosure.environment}')
    response_body += wrap(f'Open to Visitors: {enclosure.open_to_visitors}')
    
    for animal in enclosure.animals:
        response_body += wrap(f'Animal: {animal.name}')
    
    response = make_response(response_body, 200)
    return response
    
def wrap(s):
    return f'<ul>{s}</ul>'

if __name__ == '__main__':
    app.run(port=5555, debug=True)
