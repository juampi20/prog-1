from flask import Blueprint, render_template, current_app, redirect, url_for, flash
from flask_breadcrumbs import register_breadcrumb
from ..forms.user_form import UserCreateForm, UserEditForm
import requests, json

user = Blueprint("user", __name__, url_prefix="/user")

@user.route("/")
@register_breadcrumb(user, ".", "Users")
def index():
    r = requests.get(current_app.config["API_URL"]+"/users",headers={"content-type":"application/json"})
    users = json.loads(r.text)["Users"]
    title = "Users List"
    return render_template("users.html", title=title, users=users) # Mostrar template

@user.route("/view/<int:id>")
@register_breadcrumb(user,".view","View")
def view(id):
    url = current_app.config["API_URL"]+"/user/"+str(id)
    r = requests.get(url, headers={"content-type":"application/json"})
    if (r.status_code == 404):
        flash("User not found","danger")
        return redirect(url_for("user.index"))
    user = json.loads(r.text)
    title = "User View"
    return render_template("user.html", title=title, user=user)

@user.route("/create", methods=["GET", "POST"])
@register_breadcrumb(user, ".create", "Create User")
def create():
    form = UserCreateForm() # Instanciar formulario
    if form.validate_on_submit(): # Si el formulario ha sido enviado y es valido correctamente
        user = {
            "email": form.email.data,
            "password": form.password.data,
            "admin": form.admin.data
        }
        data = json.dumps(user)
        r = requests.post(current_app.config["API_URL"]+"/users",headers={"content-type":"application/json"}, data=data)
        return redirect(url_for("user.index")) # Redirecciona a la lista
    return render_template("userCreate_form.html", form=form) # Muestra el formulario

@user.route("/edit/<int:id>", methods=["GET","POST"])
@register_breadcrumb(user, ".edit", "Edit User")
def edit(id):
    form = UserEditForm()
    url = current_app.config["API_URL"]+"/user/"+str(id)
    if not form.is_submitted():
        r = requests.get(url, headers={"content-type":"application/json"})
        if (r.status_code == 404):
            flash("User not found","danger")
            return redirect(url_for("user.index"))
        user = json.loads(r.text)
        form.email.data = user["email"]
        form.admin.data = user["admin"]        

    if form.validate_on_submit():
        user = {
            "email": form.email.data,
            "admin": form.admin.data
        }
        data = json.dumps(user)
        r = requests.put(url, headers={"content-type":"application/json"}, data=data)
        flash("User edited","success")
        return redirect(url_for("user.index"))
    return render_template("userEdit_form.html", form=form, id=id)

@user.route("/delete/<int:id>")
def delete(id):
    url = current_app.config["API_URL"]+"/user/"+str(id)
    r = requests.delete(url, headers={"content-type":"application/json"})
    flash("User deleted","danger")
    return redirect(url_for("user.index"))

    
