import json

from flask import Blueprint, flash, redirect, render_template, url_for, request, flash
from flask_breadcrumbs import register_breadcrumb
from flask_login import login_required

from ..forms.sensor_form import SensorCreateForm, SensorEditForm, SensorFilterForm
from ..utilities.functions import sendRequest
from .auth import admin_required

sensor = Blueprint("sensor", __name__, url_prefix="/sensor")


@sensor.route("/")
@login_required
@admin_required
@register_breadcrumb(sensor, ".", "Sensors")
def index():
    # Eliminar la protección csrf para el formulario de filtro
    # Cargar parametros de la url en el formulario
    filter = SensorFilterForm(request.args, meta={"csrf": False})
    # Obtener usuarios
    r = sendRequest(method="get", url="/users-info")

    # Cargar usuarios en el formulario
    filter.userId.choices = [
        (int(user["id"]), user["email"]) for user in json.loads(r.text)["Users"]
    ]
    filter.userId.choices.insert(0, [0, "All"])
    data = {}
    # Aplicado de filtros
    # Validar formulario de filtro
    if filter.validate():
        if filter.userId.data != None and filter.userId.data != 0:
            data["userId"] = filter.userId.data
        if filter.name.data != None:
            data["name"] = filter.name.data
        if filter.status.data:
            data["status"] = filter.status.data
        if filter.active.data:
            data["active"] = filter.active.data

    # Ordenamiento
    if "sort_by" in request.args:
        data["sort_by"] = request.args.get("sort_by", "")

    # Numero de pagina
    if "page" in request.args:
        data["page"] = request.args.get("page", "")
    else:
        if "page" in data:
            del data["page"]

    # Obtener datos de la api
    r = sendRequest(method="get", url="/sensors", data=json.dumps(data), auth=True)

    if r.status_code == 200:
        sensors = json.loads(r.text)["sensors"]
        pagination = {}
        pagination["total"] = json.loads(r.text)["total"]
        pagination["pages"] = json.loads(r.text)["pages"]
        pagination["current_page"] = json.loads(r.text)["page"]
        title = "Sensors"
        return render_template(
            "sensors.html",
            title=title,
            sensors=sensors,
            filter=filter,
            pagination=pagination,
        )
    else:
        flash("Error de filtrado", "danger")
        return redirect(url_for("sensor.index"))


@sensor.route("/view/<int:id>")
@login_required
@admin_required
@register_breadcrumb(sensor, ".view", "Sensor")
def view(id):
    r = sendRequest(method="get", url="/sensor/" + str(id), auth=True)
    if r.status_code == 404:
        flash("Sensor not found", "danger")
        return redirect(url_for("sensor.index"))
    sensor = json.loads(r.text)
    title = "Sensor View"
    return render_template("sensor_view.html", title=title, sensor=sensor)


@sensor.route("/create", methods=["GET", "POST"])
@login_required
@admin_required
@register_breadcrumb(sensor, ".create", "Create Sensor")
def create():
    form = SensorCreateForm()  # Instanciar formulario
    if (
        form.validate_on_submit()
    ):  # Si el formulario ha sido enviado y es valido correctamente
        sensor = {
            "name": form.name.data,
            "ip": form.ip.data,
            "port": form.port.data,
            "status": form.status.data,
            "active": form.active.data,
            "userId": form.userId.data,
        }
        data = json.dumps(sensor)
        r = sendRequest(method="post", url="/sensors", data=data, auth=True)
        return redirect(url_for("sensor.index"))  # Redirecciona a la lista
    return render_template("sensor_edit.html", form=form)


@sensor.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
@register_breadcrumb(sensor, ".edit", "Edit Sensor")
def edit(id):
    form = SensorEditForm()
    req = sendRequest(method="get", url="/users-info")
    users = [(int(user["id"]), user["email"]) for user in json.loads(req.text)["Users"]]
    form.userId.choices = users
    form.userId.choices.insert(0, [0, "Select one user"])
    if not form.is_submitted():
        r = sendRequest(method="get", url="/sensor/" + str(id), auth=True)
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
            for user_id, user_email in users:
                if sensor["user"]["id"] == user_id:
                    form.userId.data = user_id
        except KeyError:
            pass

    if form.validate_on_submit():
        sensor = {
            "name": form.name.data,
            "ip": form.ip.data,
            "port": form.port.data,
            "status": form.status.data,
            "active": form.active.data,
            "userId": form.userId.data,
        }
        data = json.dumps(sensor)
        r = sendRequest(method="put", url="/sensor/" + str(id), data=data, auth=True)
        flash("Sensor edited", "success")
        return redirect(url_for("sensor.index"))

    return render_template("sensor_edit.html", id=id, form=form)


@sensor.route("/delete/<int:id>")
@login_required
@admin_required
def delete(id):
    r = sendRequest(method="delete", url="/sensor/" + str(id), auth=True)
    flash("Sensor deleted", "danger")
    return redirect(url_for("sensor.index"))
