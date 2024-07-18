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
        plants = Plant.query.all()
        response = make_response([plant.to_dict() for plant in plants],200)
        return response
    
    def post(self):
        new_plant = Plant(
            name = request.get_json()["name"],
            image = request.get_json()["image"],
            price = request.get_json()["price"]
        )
        db.session.add(new_plant)
        db.session.commit()
        response = make_response(new_plant.to_dict(),204,{"Content-Type":"application/json"})
        return response

api.add_resource(Plants,"/plants")

class PlantByID(Resource):
    def get(self,id):
        plant = Plant.query.filter(Plant.id == id).first()
        if plant:
            response = make_response(plant.to_dict(),200)
            return response
        else:
            response = make_response({"message":"Plant not found"},404)
            return response

api.add_resource(PlantByID,"/plants/<int:id>")
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
