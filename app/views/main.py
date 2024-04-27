from flask import render_template, Blueprint, request
from ..models import Product
import json
from ..map_utils import choose_map_image

bp = Blueprint(
    "main",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)


@bp.route("/mapa", methods=["GET"])
def mapa():
    # Przyjmujemy listę wolnych stolików w formacie JSON
    free_tables_json = request.args.get('free_tables', '[]')  # domyślnie pusta lista
    print(free_tables_json)
    if free_tables_json == '[]':
        return render_template("main/mapa.html", image_file="map_total.png")
    try:
        free_tables = json.loads(free_tables_json)
        # Funkcja zwracająca nazwę pliku mapy na podstawie wolnych stolików
        image_file = choose_map_image(free_tables)
    except json.JSONDecodeError:
        return "Nieprawidłowy format JSON", 400

    return render_template("main/mapa.html", image_file=image_file)


@bp.route("/")
def home():
    products = Product.query.all()
    return render_template("main/main.html")
