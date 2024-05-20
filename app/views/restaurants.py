from flask import render_template, Blueprint
from ..models import Restaurant, Product

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

@bp.route('/restaurant/<string:restaurant_name>')
def restaurant(restaurant_name):
    restaurant = Restaurant.query.filter_by(name=restaurant_name).first_or_404()
    products = Product.query.filter_by(restaurant_id=restaurant.id).all()
    return render_template('main/restaurant.html', restaurant=restaurant, products=products)