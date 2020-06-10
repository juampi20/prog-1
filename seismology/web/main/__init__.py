import os
from flask import Flask
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config['API_URL'] = os.getenv('API_URL')
    from main.routes import main, verified_seism
    app.register_blueprint(routes.main.main)
    app.register_blueprint(routes.verified_seism.verified_seism)
    return app