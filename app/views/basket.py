from flask import render_template, Blueprint


bp = Blueprint(
    "basket",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)


@bp.route("/basket")
def product_list():
    # Do some stuff
    return render_template("main/basket.html")
