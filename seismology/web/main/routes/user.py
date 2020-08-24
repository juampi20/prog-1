from flask import Blueprint, render_template, current_app, redirect, url_for
from flask_breadcrumbs import register_breadcrumb, default_breadcrumb_root
from ..forms.user_form import UserForm
import requests, json

user = Blueprint('user', __name__, url_prefix='/user')
# default_breadcrumb_root(user, '.main')

@user.route('/')
@register_breadcrumb(user, '.', 'Users')
def index():
    r = requests.get(current_app.config['API_URL']+'/users',headers={'content-type':'application/json'})
    users = json.loads(r.text)['Users']
    title = 'Users List'
    return render_template('users.html', title=title, users=users) # Mostrar template

@user.route('/create', methods=['GET', 'POST'])
@register_breadcrumb(user, '.create', 'Create User')
def create():
    form = UserForm() # Instanciar formulario
    if form.validate_on_submit(): # Si el formulario ha sido enviado y es valido correctamente
        user = {
            "email": form.email.data,
            "password": form.password.data,
            "admin": form.admin.data
        }
        data = json.dumps(user)
        print(data)
        r = requests.post(current_app.config["API_URL"]+"/users",headers={'content-type':'application/json'}, data=data)
        print(r)
        return redirect(url_for('user.index')) # Redirecciona a la lista
    return render_template('user_form.html', form=form) # Muestra el formulario
