from flask import render_template, Blueprint
from ..models import Product

bp = Blueprint(
    "products",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)


@bp.route("<int:id>/products")
def product_list(id):
    products = Product.query.all()
    return render_template("main/products.html", products=products, category="Products")


@bp.route("<int:id>/products/<category>")
def products_list(category, id):
    products = Product.query.filter_by(category=category).all()
    return render_template("main/products.html", products=products, category=category)


@bp.route("<int:id>/products/<category>/<name>")
def product(name, category, id):
    product = Product.query.filter_by(name=name).first_or_404()
    return render_template("main/product.html", product=product)
