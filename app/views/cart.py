from flask import Flask, render_template, request, redirect, url_for, Blueprint
from .. import cache
from ..models import Product  
# Konfiguracja cache


bp = Blueprint(
    "cart",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)

@bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    product = Product.query.get(product_id)
    
    if product:
        cart = cache.get('cart') or []
        cart.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'quantity': 1
        })
        cache.set('cart', cart)
    
    return redirect('/cart')

@bp.route('/cart')
def view_cart():
    cart = cache.get('cart') or []
    return render_template('main/cart.html', cart=cart)

@bp.route('/clear_cart')
def clear_cart():
    cache.set('cart', [])
    return redirect('/cart')

