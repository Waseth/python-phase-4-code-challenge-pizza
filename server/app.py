#!/usr/bin/env python3
from flask_migrate import Migrate

from models import db, Restaurant, RestaurantPizza, Pizza

from flask import Flask, request, jsonify

from flask_restful import Api, Resource

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False
#initialisation of db and migration
migrate = Migrate(app, db)

db.init_app(app)
#init flask restful Api
api = Api(app)


# Add RestaurantPizzasResource route
class RestaurantPizzasResource(Resource):
    # implementation of post functionality
    def post(self):
        """Create a new restaurant-pizza relationship."""
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
            db.session.rollback()  # Rollback the session when there is an error
            print(e)  # print the exception
            return {"errors": ["validation errors"]}, 400

        

# Add RestaurantResource route
class RestaurantResource(Resource):
    #implementation of get functionality
    def get(self, id):
        """Get one restaurant by ID."""
        restaurant = Restaurant.query.get(id)
        if restaurant is None:
            return {"error": "Restaurant not found"}, 404
        return jsonify(restaurant.to_dict(only=('id', 'name', 'address', 'restaurant_pizzas')))
    #implementation of delete functionality
    def delete(self, id):
        """Delete restaurants"""
        restaurant = Restaurant.query.get(id)
        if restaurant is None:
            return {"error": "Restaurant not found"}, 404
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204

# Add PizzasResource route
class PizzasResource(Resource):
    def get(self):
        """Retrieve pizzas."""
        pizzas = Pizza.query.all()
        return jsonify([pizza.to_dict(only=('id', 'name', 'ingredients')) for pizza in pizzas])


# Add RestaurantsResource route
class RestaurantsResource(Resource):
    def get(self):
        """Retrieve all restaurants."""
        restaurants = Restaurant.query.all()
        return jsonify([restaurant.to_dict(only=('id', 'name', 'address')) for restaurant in restaurants])

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
