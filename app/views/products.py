from flask import render_template, Blueprint
from ..models import Product

bp = Blueprint(
    "products",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)


@bp.route("/products")
def product_list():
    products = Product.query.all()
    return render_template("main/products.html", products=products)
