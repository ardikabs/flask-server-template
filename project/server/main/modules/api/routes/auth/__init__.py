
from flask_restplus import Namespace

api = Namespace("auth", description="Authentication Related Operation")

from . import resource