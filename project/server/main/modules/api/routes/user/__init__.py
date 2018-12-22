
from flask_restplus import Namespace

api = Namespace("users", description="User Related Operation")

from . import resource