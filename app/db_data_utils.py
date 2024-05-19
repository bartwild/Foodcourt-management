from . import db
from .models import Restaurant
import csv
from sqlalchemy.sql import text


def load_data():
    for restaurant in read_restaurants_file("app/static/text_files/restaurant.csv"):
        print(restaurant)
        new_restaurant = Restaurant(
            name=restaurant["name"],
            image_url=restaurant["image_url"],
            description=restaurant["description"],
        )
        db.session.add(new_restaurant)
        db.session.commit()


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


def truncate_tables():
    for table_name in db.metadata.tables:
        db.session.execute(text(f"DELETE FROM {table_name}"))
    db.session.commit()
