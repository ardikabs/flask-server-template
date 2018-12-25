
from flask_restplus import Namespace

api = Namespace("groups", description="Groups Related Operation")

from . import resource