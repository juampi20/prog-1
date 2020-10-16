import json

from flask import Blueprint, flash, redirect, render_template, url_for, request, flash
from flask_breadcrumbs import register_breadcrumb
from flask_login import login_required

from .auth import admin_required
from ..forms.seism_form import UnverifiedSeismEditForm, SeismFilterForm
from ..utilities.functions import sendRequest

unverified_seism = Blueprint(
    "unverified_seism", __name__, url_prefix="/unverified-seism"
)


@unverified_seism.route("/")
@login_required
@register_breadcrumb(unverified_seism, ".", "Unverified Seisms")
def index():
    filter = SeismFilterForm(request.args, meta={"csrf": False})

    r = sendRequest(method="get", url="/sensors-info")
    filter.sensorId.choices = [
        (int(sensor["id"]), sensor["name"]) for sensor in json.loads(r.text)["sensors"]
    ]
    filter.sensorId.choices.insert(0, [0, "All"])
    data = {}
    # Aplicado de filtros
    # Validar formulario de filtro
    if filter.validate():
        # Datetime
        if filter.datetimeFrom.data and filter.datetimeTo.data:
            if filter.datetimeFrom.data == filter.datetimeTo.data:
                data["datetime"] = filter.datetimeTo.data.strftime("%Y-%m-%d %H:%M")
        if filter.datetimeFrom.data != None:
            data["datetimeFrom"] = filter.datetimeFrom.data.strftime("%Y-%m-%d %H:%M")
        if filter.datetimeTo.data != None:
            data["datetimeTo"] = filter.datetimeTo.data.strftime("%Y-%m-%d %H:%M")

        # SensorId
        if filter.sensorId.data != None and filter.sensorId.data != 0:
            data["sensorId"] = filter.sensorId.data

        # Depth
        if filter.depth_min.data != None:
            data["depth_min"] = filter.depth_min.data
        if filter.depth_max.data != None:
            data["depth_max"] = filter.depth_max.data

        # Magnitude
        if filter.magnitude_min.data != None:
            data["magnitude_min"] = filter.magnitude_min.data
        if filter.magnitude_max.data != None:
            data["magnitude_max"] = filter.magnitude_max.data

    # Ordenamiento
    if "sort_by" in request.args:
        data["sort_by"] = request.args.get("sort_by", "")

    # Numero de pagina
    if "page" in request.args:
        data["page"] = request.args.get("page", "")

    # Obtener datos de la api para la tabla
    r = sendRequest(
        method="get", url="/unverified-seisms", data=json.dumps(data), auth=True
    )

    if r.status_code == 200:
        unverified_seisms = json.loads(r.text)["Unverified-seisms"]
        # Cargar datos de paginacion
        pagination = {}
        pagination["total"] = json.loads(r.text)["total"]
        pagination["pages"] = json.loads(r.text)["pages"]
        pagination["current_page"] = json.loads(r.text)["page"]
        title = "Unverified Seisms List"
        return render_template(
            "unverified-seisms.html",
            title=title,
            unverified_seisms=unverified_seisms,
            filter=filter,
            pagination=pagination,
        )
    else:
        flash("Error de filtrado", "danger")
        return redirect(url_for("unverified_seism.index"))


@unverified_seism.route("/view/<int:id>")
@login_required
@register_breadcrumb(unverified_seism, ".view", "Unverified Seism")
def view(id):
    r = sendRequest(method="get", url="/unverified-seism/" + str(id), auth=True)
    if r.status_code == 404:
        flash("Seism not found", "danger")
        return redirect(url_for("unverified_seism.index"))
    unverified_seism = json.loads(r.text)
    title = "Unverified Seism View"
    return render_template(
        "unverified-seism.html", title=title, unverified_seism=unverified_seism
    )


@unverified_seism.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@register_breadcrumb(unverified_seism, ".edit", "Edit Unverified Seism")
def edit(id):
    form = UnverifiedSeismEditForm()
    if not form.is_submitted():
        r = sendRequest(method="get", url="/unverified-seism/" + str(id), auth=True)
        if r.status_code == 404:
            flash("Unvrified Seism not found", "danger")
            return redirect(url_for("unverified_seism.index"))
        unverified_seism = json.loads(r.text)
        form.depth.data = unverified_seism["depth"]
        form.magnitude.data = unverified_seism["magnitude"]
        form.verified.data = unverified_seism["verified"]

    if form.validate_on_submit():
        unverified_seism = {
            "depth": form.depth.data,
            "magnitude": form.magnitude.data,
            "verified": form.verified.data,
        }
        data = json.dumps(unverified_seism)
        r = sendRequest(
            method="put", url="/unverified-seism/" + str(id), data=data, auth=True
        )
        flash("Unverified Seism edited", "success")
        return redirect(url_for("unverified_seism.index"))
    return render_template("unverfied-seismEdit_form.html", form=form, id=id)


@unverified_seism.route("/delete/<int:id>")
@login_required
def delete(id):
    r = sendRequest(method="delete", url="/unverified-seism/" + str(id), auth=True)
    flash("Unverified Seism deleted", "danger")
    return redirect(url_for("unverified_seism.index"))


@unverified_seism.route("/create", methods=["GET", "POST"])
@login_required
@admin_required
@register_breadcrumb(unverified_seism, ".create", "Create Sensor")
def create():
    r = sendRequest(method="post", url="/unverified-seisms", auth=True)
    return redirect(url_for("unverified_seism.index"))  # Redirecciona a la lista