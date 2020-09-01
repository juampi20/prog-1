from flask import Blueprint, render_template, current_app, redirect, url_for
from flask_breadcrumbs import register_breadcrumb
import requests, json

sensor = Blueprint("sensor", __name__, url_prefix="/sensor")

@sensor.route("/")
@register_breadcrumb(sensor,".","Sensors")
def index():
    r = requests.get(current_app.config["API_URL"]+"/sensors",headers={"content-type":"application"})
    sensors = json.loads(r.text)["sensors"]
    title = "Sensors"
    return render_template("sensors.html",title=title,sensors=sensors)
