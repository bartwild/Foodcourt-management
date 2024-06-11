from flask import render_template, Blueprint
from ..models import Restaurant, Product

bp = Blueprint(
    "restaurants",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)


@bp.route("<int:id>/restaurants")
def product_list(id):
    restaurants = Restaurant.query.all()
    return render_template("main/restaurants.html", restaurants=restaurants, id=id)


@bp.route("<int:id>/restaurant/<string:restaurant_name>")
def restaurant(restaurant_name, id):
    restaurant = Restaurant.query.filter_by(name=restaurant_name).first_or_404()
    products = Product.query.filter_by(restaurant_id=restaurant.id).all()
    return render_template("main/restaurant.html", restaurant=restaurant, products=products, id=id)
