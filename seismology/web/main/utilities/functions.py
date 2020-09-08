from flask import request, current_app, redirect, url_for, flash
from werkzeug.routing import RequestRedirect
import requests
import json


def sendRequest(method, url, auth=False, data=None):
    #Headers por defecto
    headers = { "content-type": "application/json" }
    
    #Verificamos si necesita autorizacion
    if auth == True:
        #Recolectamos el token de las cookies
        token = request.cookies['access_token']
        #Incorporamos el token en el headers
        headers["authorization"] = "Bearer "+token

    if method.lower() == "get":
        r = requests.get(
            current_app.config["API_URL"] + url,
            headers=headers,
            data=data
        )
        

    if method.lower() == "post":
        r = requests.post(
            current_app.config["API_URL"] + url,
            headers=headers,
            data=data
        )


    if method.lower() == "put":
        r = requests.put(
            current_app.config["API_URL"] + url,
            headers=headers,
            data=data
        )


    if method.lower() == "delete":
        r = requests.delete(
            current_app.config["API_URL"] + url,
            headers=headers
        )


    if r.status_code == 401 or r.status_code == 422:
        flash("Authorization token not valid. Please log in again", "warning")
        raise RequestRedirect(url_for("main.logout"))

    return r
    