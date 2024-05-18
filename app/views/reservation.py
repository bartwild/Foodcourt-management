from flask import render_template, Blueprint


bp = Blueprint(
    "reservation",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)


@bp.route("/reservation")
def product_list():
    # Do some stuff
    return render_template("main/reservation.html")
