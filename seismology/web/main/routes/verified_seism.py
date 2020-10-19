import json, io, csv
from datetime import datetime

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
    flash,
    make_response,
)
from flask_breadcrumbs import register_breadcrumb

from ..forms.login_form import LoginForm
from ..forms.seism_form import SeismFilterForm
from ..utilities.functions import sendRequest

verified_seism = Blueprint("verified_seism", __name__, url_prefix="/verified-seism")


@verified_seism.route("/")
@register_breadcrumb(verified_seism, ".", "Verified Seisms")
def index():
    loginForm = LoginForm()
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

    if "download" in request.args:
        if request.args.get("download", "") == "Download":
            code = 200
            # Comenzar por la primera pagina
            page = 1
            list_seisms = []
            # Recorrer hasta que no haya mas paginas
            while code == 200:
                data["page"] = page
                # Llamada a la api
                r = sendRequest(
                    method="get",
                    url="/verified-seisms",
                    data=json.dumps(data),
                )
                code = r.status_code
                if code == 200:
                    # Recorrer los sismos de la pagina y colocar los campos que se quieren agregar
                    for seism in json.loads(r.text)["Verified-seisms"]:
                        element = {
                            "datetime": seism["datetime"],
                            "depth": seism["depth"],
                            "magnitude": seism["magnitude"],
                            "latitude": seism["latitude"],
                            "longitude": seism["longitude"],
                            "sensor.name": seism["sensor"]["name"],
                        }
                        # Agregar cada elemento a la lista
                        list_seisms.append(element)
                # Aumentar en uno el numero de pagina
                page += 1

            # Inicializar para poder escribir en el buffer de memoria
            si = io.StringIO()
            # Inicializar el objeto que va a escribir el csv a partir de un diccionario
            # Pasar las claves del diccionario como cabecera
            fc = csv.DictWriter(si, fieldnames=list_seisms[0].keys())
            # Escribir la cabecera
            fc.writeheader()
            # Escribir las filas
            fc.writerows(list_seisms)

            # Crear una respuesta que tiene como contenido el valor dedl buffer
            output = make_response(si.getvalue())
            # Colocar cabeceras para que se descargue como un archivo
            output.headers["Content-Disposition"] = "attachment; filename=seisms.csv"
            output.headers["Content-type"] = "text/csv"
            # Devolver la salida
            return output

    # Numero de pagina
    if "page" in request.args:
        data["page"] = request.args.get("page", "")
    else:
        if "page" in data:
            del data["page"]

    # Obtener datos de la api para la tabla
    r = sendRequest(
        method="get",
        url="/verified-seisms",
        data=json.dumps(data),
    )

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
