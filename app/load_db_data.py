from . import db
from .models import Restaurant
import csv


def load_data():
    # restaurant1 = Restaurant(
    #     name="Pasta Palace",
    #     image_url="static/images/food/pizzeria.jpg",
    #     description="A cozy place with the best pasta in town.",
    # )
    # restaurant2 = Restaurant(
    #     name="Burger Barn",
    #     image_url="static/images/food/burgerownia.jpg",
    #     description="Juicy burgers and crispy fries.",
    # )
    for restaurant in read_restaurants_file("app/static/text_files/restaurants.csv"):
        print(restaurant)
        new_restaurant = Restaurant(
            name=restaurant["name"],
            image_url=restaurant["image_url"],
            description=restaurant["description"],
        )
        db.session.add(new_restaurant)
        db.session.commit()

    # db.session.add(restaurant1)
    # db.session.add(restaurant2)
    # db.session.commit()


def read_restaurants_file(file_path):
    restaurants = []

    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            restaurant = {
                "name": row["name"],
                "image_url": row["image_url"],
                "description": row["description"],
            }
            restaurants.append(restaurant)

    return restaurants
