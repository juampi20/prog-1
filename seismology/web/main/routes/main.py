from flask import Blueprint, redirect, url_for
from . import verified_seism

main = Blueprint("main", __name__, url_prefix="/")

@main.route("/")
def index():
    return redirect(url_for("verified_seism.index"))