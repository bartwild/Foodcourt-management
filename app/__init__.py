from flask import Flask
from flask_socketio import SocketIO
from .config import Config

socketio = SocketIO()  # Tworzymy globalną instancję SocketIO


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    from .views import main, cart, products
    from .database import db
    db.init_app(app)

    with app.app_context():
        db.create_all()
        print("Db created")
    socketio.init_app(app)
    app.register_blueprint(main.bp)
    app.register_blueprint(cart.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(start.bp)

    return app
