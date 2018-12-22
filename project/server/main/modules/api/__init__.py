from flask import Blueprint
from flask_restplus import Api, abort

api_v1 = Api(
    title="GDN INFRASTRUCTURE MANAGER CLOUD API",
    version="0.1.2"
)

def init_app(app, **kwargs):
    blueprint = Blueprint("api", __name__, url_prefix="/api/v1")

    from . import (
        routes,
        http_exceptions,
        util
    )
    routes.setup(api_v1)

    api_v1.init_app(blueprint)
    app.register_blueprint(blueprint)