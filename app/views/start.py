from flask import render_template, Blueprint
import os


bp = Blueprint(
    "start",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)


@bp.route("<int:id>/")
def start(id):
    return render_template("start.html")
