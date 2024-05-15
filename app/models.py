from flask_sqlalchemy import SQLAlchemy

from . import db


class Restaurant(db.Model):
    __tablename__ = "restaurant"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200))
    description = db.Column(db.String(500), nullable=True)

    products = db.relationship("Product", backref="restaurant", lazy=True)


class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    restaurant_id = db.Column(
        db.Integer, db.ForeignKey("restaurant.id"), nullable=False
    )
