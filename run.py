# run.py or similar
from app import create_app, socketio, db  # Załóżmy, że twoje funkcje importujące są poprawne
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)
if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', debug=True)
