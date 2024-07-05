from sqlalchemy.ext.associationproxy import association_proxy

from sqlalchemy.orm import validates

from sqlalchemy import MetaData

from sqlalchemy_serializer import SerializerMixin

from flask_sqlalchemy import SQLAlchemy

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    # add relationships
    pizza_id = db.Column(db.Integer, db.ForeignKey("pizzas.id"), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"), nullable=False)
    # add serialization rules
    serialize_rules = ("-restaurant.restaurant_pizzas", "-pizza.restaurant_pizzas")
    # add validation
    @validates('price')
    def validate_price(self, key, value):
        if value < 1 or value > 30:
            raise ValueError("Price must be between 1 and 30")
        return value
    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"
class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # add relationship
    restaurant_pizzas = db.relationship("RestaurantPizza", backref="pizza")
    restaurants = association_proxy("restaurant_pizzas", "restaurant")
    # add serialization rules
    serialize_rules = ("-restaurant_pizzas.pizza", "-restaurant_pizzas.restaurant")
    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    # add relationship
    restaurant_pizzas = db.relationship("RestaurantPizza", backref="restaurant", cascade="all, delete-orphan")
    pizzas = association_proxy("restaurant_pizzas", "pizza")
    # add serialization rules
    serialize_rules = ("-restaurant_pizzas.restaurant", "-restaurant_pizzas.pizza", "restaurant_pizzas")


    def __repr__(self):
        return f"<Restaurant {self.name}>"



