__author__ = "Ardika Bagus Saputro"
__copyright__ = "Copyright 2018, Flask Server Template"

__version__ = "0.0.1"
__maintainer__ = "Ardika Bagus Saputro"
__email__ = "ardikabs@gmail.com"
__status__ = "Development"

from server.app import create_app, configure_logger
from server.extensions.celery import create_celery
from server import main


def make_server(config_name=None, gunicorn=False):
    application = create_app(config_name)
    configure_logger(application, gunicorn=gunicorn)

    main.init_app(application)
    application.app_context().push()
    return application

def make_worker(config_name=None):
    application = create_app(config_name)
    application.app_context().push()

    celery = create_celery(application)
    from server.extensions.celery import tasks
    tasks.setup()

    return celery