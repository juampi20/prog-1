import json

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_breadcrumbs import register_breadcrumb
from flask_login import login_required

from ..forms.sensor_form import SensorCreateForm, SensorEditForm
from ..utilities.functions import sendRequest
from .auth import admin_required

sensor = Blueprint("sensor", __name__, url_prefix="/sensor")


@sensor.route("/")
@login_required
@admin_required
@register_breadcrumb(sensor, ".", "Sensors")
def index():
    r = sendRequest(method="get",
                    url="/sensors",
                    auth=True)
    sensors = json.loads(r.text)["sensors"]
    title = "Sensors"
    return render_template("sensors.html",
                           title=title,
                           sensors=sensors)


@sensor.route("/view/<int:id>")
@login_required
@admin_required
@register_breadcrumb(sensor, ".view", "Sensor")
def view(id):
    r = sendRequest(method="get",
                    url="/sensor/" + str(id),
                    auth=True)
    if (r.status_code == 404):
        flash("Sensor not found", "danger")
        return redirect(url_for("sensor.index"))
    sensor = json.loads(r.text)
    title = "Sensor View"
    return render_template("sensor.html",
                           title=title,
                           sensor=sensor)


@sensor.route("/create", methods=["GET", "POST"])
@login_required
@admin_required
@register_breadcrumb(sensor, ".create", "Create Sensor")
def create():
    form = SensorCreateForm()  # Instanciar formulario
    if form.validate_on_submit():  # Si el formulario ha sido enviado y es valido correctamente
        sensor = {
            "name": form.name.data,
            "ip": form.ip.data,
            "port": form.port.data,
            "status": form.status.data,
            "active": form.active.data,
            "userId": form.userId.data,
        }
        data = json.dumps(sensor)
        r = sendRequest(method="post",
                        url="/sensors",
                        data=data,
                        auth=True)
        return redirect(url_for("sensor.index"))  # Redirecciona a la lista
    return render_template("sensorEdit_form.html", form=form)


@sensor.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
@register_breadcrumb(sensor, ".edit", "Edit Sensor")
def edit(id):
    form = SensorEditForm()
    req = sendRequest(method="get",
                      url="/users",
                      auth=True)
    users = json.loads(req.text)["Users"]
    users_list = [(0, "Select one user email")]
    for user in users:
        users_list.append((user["id"], user["email"]))
    form.userId.choices = users_list
    print(users_list)
    if not form.is_submitted():
        r = sendRequest(method="get",
                        url="/sensor/"+str(id),
                        auth=True)
        if r.status_code == 404:
            flash("Sensor not found", "danger")
            return redirect(url_for("sensor.index"))
        sensor = json.loads(r.text)

        # Load data
        form.name.data = sensor["name"]
        form.ip.data = sensor["ip"]
        form.port.data = sensor["port"]
        form.status.data = sensor["status"]
        form.active.data = sensor["active"]

        # Load users
        try:
            user = sensor["user"]
            for user_id, email in users_list:
                if user_id == int(user["id"]):
                    form.userId.data = int(user_id)
        except KeyError:
            pass

    if form.validate_on_submit():
        sensor = {
            "name": form.name.data,
            "ip": form.ip.data,
            "port": form.port.data,
            "status": form.status.data,
            "active": form.active.data,
            "userId": form.userId.data
        }
        data = json.dumps(sensor)
        r = sendRequest(method="put",
                        url="/sensor/" + str(id),
                        data=data,
                        auth=True)
        flash("Sensor edited", "success")
        return redirect(url_for("sensor.index"))

    return render_template("sensorEdit_form.html",
                           id=id,
                           form=form)


@sensor.route("/delete/<int:id>")
@login_required
@admin_required
def delete(id):
    r = sendRequest(method="delete",
                    url="/sensor/"+str(id),
                    auth=True)
    flash("Sensor deleted", "danger")
    return redirect(url_for("sensor.index"))
