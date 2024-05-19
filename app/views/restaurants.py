from flask import render_template, Blueprint
from ..models import Restaurant

bp = Blueprint(
    "restaurants",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)


@bp.route("/restaurants")
def product_list():
    restaurants = Restaurant.query.all()
    return render_template("main/restaurants.html", restaurants = restaurants)
