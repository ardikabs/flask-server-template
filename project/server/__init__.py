
__author__ = 'Ardika Bagus Saputro <ardika.saputro@gdn-commerce.com>'
__version__ = '0.1.2'

from server.app import create_app, configure_logger
from server.extensions.celery import create_celery
from server import main


def make_server(config_name=None, gunicorn=False):
    application = create_app(config_name)
    configure_logger(application, gunicorn=gunicorn)
    main.init_app(application)
    application.app_context().push()
    return application

def make_worker(config_name=None, gunicorn=False):
    application = create_app()
    application.app_context().push()

    celery = create_celery(application)

    from server.extensions.celery import tasks
    tasks.setup()
    return celery