import json
from datetime import datetime

from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_breadcrumbs import register_breadcrumb

from ..forms.login_form import LoginForm
from ..forms.seism_form import VerifiedSeismFilterForm
from ..utilities.functions import sendRequest

verified_seism = Blueprint("verified_seism", __name__, url_prefix="/verified-seism")


@verified_seism.route("/")
@register_breadcrumb(verified_seism, ".", "Verified Seisms")
def index():
    loginForm = LoginForm()
    filter = VerifiedSeismFilterForm(request.args, meta={"csrf": False})

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
        if filter.depth.data != None:
            data["depth"] = filter.depth.data

        # Magnitude
        if filter.magnitude.data != None:
            data["magnitude"] = filter.magnitude.data

    # Ordenamiento
    if "sort_by" in request.args:
        data["sort_by"] = request.args.get("sort_by", "")

    # Numero de pagina
    if "page" in request.args:
        data["page"] = request.args.get("page", "")
    else:
        if "page" in data:
            del data["page"]

    # Obtener datos de la api para la tabla
    print(data)
    r = sendRequest(method="get", url="/verified-seisms", data=json.dumps(data))

    if r.status_code == 200:
        # Cargar sismos verificados
        verified_seisms = json.loads(r.text)["Verified-seisms"]
        # Cargar datos de paginacion
        pagination = {}
        pagination["total"] = json.loads(r.text)["total"]
        pagination["pages"] = json.loads(r.text)["pages"]
        pagination["current_page"] = json.loads(r.text)["page"]
        title = "Verified Seisms List"
        return render_template(
            "verified-seisms.html",
            title=title,
            verified_seisms=verified_seisms,
            loginForm=loginForm,
            filter=filter,
            pagination=pagination,
        )
    else:
        flash("Error de filtrado", "danger")
        return redirect(url_for("verified_seism.index"))


@verified_seism.route("/view/<int:id>")
@register_breadcrumb(verified_seism, ".view", "View")
def view(id):
    r = sendRequest(method="get", url="/verified-seism/" + str(id))
    if r.status_code == 404:
        return redirect(url_for("verified_seism.index"))  # Mostrar template
    verified_seism = json.loads(r.text)
    title = "Verified Seism View"
    loginForm = LoginForm()
    return render_template(
        "verified-seism.html",
        title=title,
        verified_seism=verified_seism,
        loginForm=loginForm,
    )  # Mostrar template
