
from . import api
from flask_restplus import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    get_jwt_identity
)
from flask_restplus import Resource
from server.main.models import UserModel, BlacklistedTokenModel


from . import api
from .serializer import *
from .schema import *


from ...http_exceptions import *
from ...parser import *

pagination.args.extend(jwt_parser.args)

@api.route("/")
class UserCollection(Resource):

    @api.marshal_with(user_response, code=200)
    @api.expect(pagination, validate=True)
    @jwt_required
    def get(self):
        """
        Display All User
        """
        parser = pagination.parse_args() 
        offset = parser.offset
        limit = parser.limit
        users = UserModel.query.order_by(UserModel.id).offset(offset).limit(limit).all()
        schema = UserSchema(many=True)
        return schema.dump_response(users)

    @api.marshal_with(user_response, code=201)
    @api.expect(user_field, validate=True)
    @api.doc(parser=None)
    def post(self):
        """
        Add a new user
        """
        data = api.payload
        schema = UserSchema()
        user, err = schema.load(data)
        if err: 
            raise BadRequestError(err)

        return schema.dump_response(user)

@api.route("/<string:id>/")
@api.doc(parser=jwt_parser)
class UserItem(Resource):

    @jwt_required
    def get(self, id):
        """ Show Detail User by Selected User ID """
        identity = get_jwt_identity()
        claims = get_jwt_claims()
        print(identity)
        print(claims)
        return {}

    @jwt_required
    def put(self, id):
        """ Update User Information by Selected User ID """

        return {}

    @jwt_required
    def delete(self, id):
        """ Delete User by Selected User ID """
        return {}

