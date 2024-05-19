from . import db
from .models import Restaurant, Product
import csv
from sqlalchemy.sql import text
import os

TABLE_CLASS_MAPPING = {
    "restaurant": Restaurant,
    "product": Product,
}


def load_data():
    for table_name, model_class in TABLE_CLASS_MAPPING.items():
        file_path = f"app/static/text_files/{table_name}.csv"
        if os.path.exists(file_path):
            for data in read_table_file(file_path, model_class):
                new_object = model_class(**data)
                db.session.add(new_object)
            db.session.commit()


def read_table_file(file_path, model_class):
    objects = []
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if model_class == Product:
                try:
                    # Get the restaurant ID from the restaurant name
                    restaurant = Restaurant.query.filter_by(
                        name=row["restaurant_name"]
                    ).first()
                    if not restaurant:
                        raise ValueError(
                            f"Restaurant '{row['restaurant_name']}' not found."
                        )
                    row["restaurant_id"] = restaurant.id
                    del row["restaurant_name"]
                except Exception as e:
                    print(f"Error processing row {row}: {e}")
                    continue
            objects.append(row)
    return objects


def truncate_tables():
    db.session.execute(text("SET session_replication_role = 'replica';"))

    for table_name in reversed(db.metadata.sorted_tables):
        db.session.execute(text(f"TRUNCATE TABLE {table_name} CASCADE"))

    db.session.execute(text("SET session_replication_role = 'origin';"))

    for table in db.metadata.tables.values():
        if hasattr(table.columns, "id"):
            sequence_name = f"{table.name}_id_seq"
            db.session.execute(text(f"ALTER SEQUENCE {sequence_name} RESTART WITH 1"))

    db.session.commit()
