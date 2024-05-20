from flask import render_template, Blueprint, Flask, jsonify
import threading
import time

app = Flask(__name__)


bp = Blueprint(
    "timer",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/timer",
)


@bp.route("/")
def timer():
    return render_template("timer/timer.html")


@bp.route("/wait")
def wait_for_order():
    return render_template("timer/wait_for_order.html")
