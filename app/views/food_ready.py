from flask import render_template, Blueprint


bp = Blueprint(
    "food_ready",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)


@bp.route("/food_ready")
def product_list():
    # Do some stuff
    return render_template("main/food_ready.html")
