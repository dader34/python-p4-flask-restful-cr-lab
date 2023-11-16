#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        return jsonify([plant.to_dict() for plant in Plant.query.all()])
    
    def post(self):
        try:
            image = request.json.get("image")
            name = request.json.get("name")
            price = request.json.get("price")
            plant = Plant(image=image,name=name,price=price)
            db.session.add(plant)
            db.session.commit()
        except Exception as e:
            return {"error":e.args}

api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self,id):
        try:
            return jsonify(db.session.get(Plant, id).to_dict())
        except Exception as e:
            return {"error":e.args}
    
api.add_resource(PlantByID, '/plants/<int:id>')
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
