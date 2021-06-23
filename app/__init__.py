from flask import Flask, Blueprint
from flask_restx import Api
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

# API Auth definition dictionary
auths = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}
bp = Blueprint('api', __name__, url_prefix='/sponsor/api')
admin_bp = Blueprint('admin_api', __name__, url_prefix='/admin/api')
api = Api(bp, authorizations=auths)
admin_api = Api(admin_bp, authorizations=auths)

app.register_blueprint(bp)
app.register_blueprint(admin_bp)

from app import routes
from app import api_routes
