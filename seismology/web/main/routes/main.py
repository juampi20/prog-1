from flask import Blueprint, redirect, url_for
from flask_breadcrumbs import register_breadcrumb
from . import verified_seism

main = Blueprint("main", __name__, url_prefix="/")

@main.route("/")
@register_breadcrumb(main, 'breadcrumbs.', 'Home')
def index():
    return redirect(url_for("verified_seism.index"))