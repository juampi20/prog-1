from flask import Blueprint, render_template, current_app, redirect, url_for
from flask_breadcrumbs import register_breadcrumb, default_breadcrumb_root
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
