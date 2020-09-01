from flask import Blueprint, render_template, current_app, redirect, url_for, flash
from flask_breadcrumbs import register_breadcrumb
from ..forms.unverified_seism_form import UnverifiedSeismEditForm
import requests, json

unverified_seism = Blueprint("unverified_seism", __name__, url_prefix="/unverified-seism")

@unverified_seism.route("/")
@register_breadcrumb(unverified_seism, ".", "Unverified Seisms")
def index():
    url = current_app.config["API_URL"]+"/unverified-seisms"
    r = requests.get(url, headers={"content-type":"application/json"})
    unverified_seisms = json.loads(r.text)["Unverified-seisms"]
    title = "Unverified Seisms List"
    return render_template("unverified-seisms.html", title=title, unverified_seisms=unverified_seisms)

@unverified_seism.route("/view/<int:id>")
@register_breadcrumb(unverified_seism, ".view", "Unverified Seism")
def view(id):
    url = current_app.config["API_URL"]+"/unverified-seism/"+str(id)
    r = requests.get(url, headers={"content-type":"application/json"})
    if (r.status_code == 404):
        flash("Seism not found", "danger")
        return redirect(url_for("unverified_seism.index"))
    unverified_seism = json.loads(r.text)
    title = "Unverified Seism View"
    return render_template("unverified-seism.html", title=title, unverified_seism=unverified_seism)

@unverified_seism.route("/edit/<int:id>", methods=["GET","POST"])
@register_breadcrumb(unverified_seism, ".edit", "Edit Unverified Seism")
def edit(id):
    form = UnverifiedSeismEditForm()
    url = current_app.config["API_URL"]+"/unverified-seism/"+str(id)
    if not form.is_submitted():
        r = requests.get(url, headers={"content-type":"application/json"})
        if (r.status_code == 404):
            flash("Unvrified Seism not found","danger")
            return redirect(url_for("unverified_seism.index"))
        unverified_seism = json.loads(r.text)
        form.verified.data = unverified_seism["verified"]

    if form.validate_on_submit():
        unverified_seism = {
            "verified": form.verified.data,
        }
        data = json.dumps(unverified_seism)
        r = requests.put(url, headers={"content-type":"application/json"}, data=data)
        flash("Unverified Seism edited","success")
        return redirect(url_for("unverified_seism.index"))
    return render_template("unverfied-seismEdit_form.html", form=form, id=id)

