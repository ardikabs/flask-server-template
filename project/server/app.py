import os
import logging
from config import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def configure_logger(app, gunicorn=False):
    if gunicorn:
        gunicorn_logger = logging.getLogger("gunicorn.error")
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)
        
    else:
        root = logging.getLogger()
        handler = logging.StreamHandler()
        fmt = logging.Formatter(
            fmt='%(asctime)s %(levelname)s (%(name)s) %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S'            
        )
        handler.setFormatter(fmt)
        root.addHandler(handler)

        if app.debug:
            root.setLevel(logging.DEBUG)
        else:
            root.setLevel(logging.INFO)


def create_app(config_name=None):
    app = Flask(__name__)
    
    env_config_name = os.environ.get("FLASK_CONFIG")
    if not env_config_name and config_name is None:
        config_name = "default"
    elif env_config_name:
        config_name = env_config_name

    try:
        app.config.from_object(config[config_name])
        config[config_name].init_app(app)
    except ImportError:
        if config_name == "default":
            app.logger.error(
                "You need to set application config name. If you may want to develope apps in local environment"
                "Alternatively you can set on environment variable"
                "with name `FLASK_CONFIG` one of the following options: development, testing, production"
            )

    db.init_app(app)
    ma.init_app(app)

    return app