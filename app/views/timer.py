from flask import render_template, Blueprint, Flask, jsonify
import threading
import time

app = Flask(__name__)


bp = Blueprint(
    "timer",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)


@bp.route("<int:id>/timer/")
def timer(id):
    return render_template("timer/timer.html", id=id)


@bp.route("<int:id>/timer/wait")
def wait_for_order(id):
    return render_template("timer/wait_for_order.html", id=id)
