from flask import Flask
from flask_socketio import SocketIO
from .config import Config
from flask_migrate import Migrate
from .database import db
from .db_data_utils import load_data, truncate_tables

socketio = SocketIO()  # Tworzymy globalną instancję SocketIO


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    from .views import (
        main,
        cart,
        products,
        start,
        restaurants,
        timer,
        basket,
        food_ready,
    )
    from .database import db

    migrate = Migrate(app, db)
    db.init_app(app)

    with app.app_context():
        db.create_all()
        truncate_tables()
        load_data()
    socketio.init_app(app)

    from .views import main

    app.register_blueprint(start.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(cart.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(timer.bp)
    app.register_blueprint(restaurants.bp)
    app.register_blueprint(basket.bp)
    app.register_blueprint(food_ready.bp)

    return app
