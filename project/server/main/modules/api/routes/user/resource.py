
from . import api
from flask_restplus import Resource

@api.route("/")
class UserCollection(Resource):

    def get(self):
        """
        Display All User
        """
        return {}

