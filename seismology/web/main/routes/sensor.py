from flask import Blueprint, render_template, current_app, redirect, url_for
from flask_breadcrumbs import register_breadcrumb
import requests, json
from flask_login import login_required, LoginManager
from ..utilities.functions import sendRequest
from .auth import admin_required

sensor = Blueprint("sensor", __name__, url_prefix="/sensor")

@sensor.route("/")
@login_required
@admin_required
@register_breadcrumb(sensor,".","Sensors")
def index():
    # r = requests.get(current_app.config["API_URL"]+"/sensors",headers={"content-type":"application"})
    r = sendRequest(method="get", url="/sensors", auth=True)
    sensors = json.loads(r.text)["sensors"]
    title = "Sensors"
    return render_template("sensors.html",title=title,sensors=sensors)
