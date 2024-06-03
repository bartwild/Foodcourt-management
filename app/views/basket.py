from flask import request, redirect, url_for, render_template, Blueprint, session
from uuid import uuid4
from .. import cache
from ..models import Product, Restaurant

bp = Blueprint(
    "basket",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)


@bp.before_request
def before_request():
    if "session_id" not in session:
        session["session_id"] = str(uuid4())


@bp.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    product_id = request.form.get("product_id")
    product = Product.query.get(product_id)
    restaurant = Restaurant.query.get(product.restaurant_id)

    if product:
        cart_key = f'cart_{session["session_id"]}'

        cart = cache.get(cart_key) or []
        cart.append(
            {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "quantity": 1,
                "restaurant": restaurant.name,
            }
        )
        cache.set(cart_key, cart)

    return redirect("/basket")


@bp.route("/basket")
def view_cart():
    cart_key = f'cart_{session["session_id"]}'

    cart = cache.get(cart_key) or []
    return render_template("main/basket.html", cart=cart)


@bp.route("/basket/clear_cart")
def clear_cart():
    cart_key = f'cart_{session["session_id"]}'

    cache.set(cart_key, [])
    return redirect("/basket")


@bp.route("/basket/remove/<int:item_id>", methods=["POST"])
def remove_item(item_id):
    cart_key = f'cart_{session["session_id"]}'
    cart = cache.get(cart_key) or []

    is_removed = 0
    new_cart = cache.get(cart_key) or []
    new_cart.clear()
    for item in cart:
        print(item)
        if item["id"] != item_id or is_removed == 1:
            new_cart.append(item)

        if item["id"] == item_id and is_removed == 0:
            is_removed = 1
            continue

    cache.set(cart_key, new_cart)
    return redirect("/basket")
