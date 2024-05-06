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


def start_timer():
    print("Timer started!")
    time.sleep(10)  # Timer na 10 sekund
    print("Timer completed!")


@bp.route("/complete")
def timer_complete():
    return render_template("timer/timer_complete.html")


@bp.route("/")
def timer():
    return render_template("timer/timer.html")
