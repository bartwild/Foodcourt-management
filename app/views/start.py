from flask import render_template, Blueprint
import os


bp = Blueprint(
    "start",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)


@bp.route("/")
def start():
    burger = os.path.join('static','images','food','burger.jpg')
    return render_template("start.html", burg = burger)