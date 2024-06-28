#!/usr/bin/env python3
from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Restaurant, RestaurantPizza, Pizza
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

# Add RestaurantsResource route
class RestaurantsResource(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        return jsonify([restaurant.to_dict(only=('id', 'name', 'address')) for restaurant in restaurants])
# Add RestaurantResource route
class RestaurantResource(Resource):
    #implementation of get functionality
    def get(self, id):
        restaurant = Restaurant.query.get(id)
        if restaurant is None:
            return {"error": "Restaurant not found"}, 404
        return jsonify(restaurant.to_dict(only=('id', 'name', 'address')))
    #implementation of delete functionality
    def delete(self, id):
        restaurant = Restaurant.query.get(id)
        if restaurant is None:
            return {"error": "Restaurant not found"}, 404
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204

# Add PizzasResource route
class PizzasResource(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        return jsonify([pizza.to_dict(only=('id', 'name', 'ingredients')) for pizza in pizzas])


# Add RestaurantPizzasResource route
class RestaurantPizzasResource(Resource):
    # implementation of post functionality
    def post(self):
        data = request.get_json()
        try:
            new_restaurant_pizza = RestaurantPizza(
                price=data["price"],
                pizza_id=data["pizza_id"],
                restaurant_id=data["restaurant_id"]
            )
            db.session.add(new_restaurant_pizza)
            db.session.commit()
            return jsonify(new_restaurant_pizza.to_dict()), 201
        except Exception as e:
            return {"errors": ["validation errors"]}, 400
# Real addition of the routes
api.add_resource(RestaurantsResource, '/restaurants')
api.add_resource(RestaurantResource, '/restaurants/<int:id>')
api.add_resource(PizzasResource, '/pizzas')
api.add_resource(RestaurantPizzasResource, '/restaurant_pizzas')

@app.route("/")
def index():
    return "<h1>Code challenge</h1>"


if __name__ == "__main__":
    app.run(port=5555, debug=True)
