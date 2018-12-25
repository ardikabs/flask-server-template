
from server.app import ma, jwt
from flask_jwt_extended import (
    jwt_required,
    jwt_refresh_token_required,
    create_access_token, 
    create_refresh_token,
    get_raw_jwt,
    get_jwt_identity
)
from flask_restplus import Resource
from server.main.models import UserModel, BlacklistedTokenModel

from . import api
from .serializer import *


from ...http_exceptions import *
from ...parser import *

@jwt.user_identity_loader
def set_user_identity(user):
    return user.id

@jwt.user_claims_loader
def add_claim_to_access_token(user):
    return {
        "role": user.role.name,
        "groups": [group.user_role for group in user.groups_membership]
    }

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    print(jti)
    blacklisted = BlacklistedTokenModel.get(jti)
    if not blacklisted:
        return False
    return True

@api.route("/login/")
class Login(Resource):

    @api.marshal_with(login_response, code=200)
    @api.expect(user_login_field, validate=True)
    def post(self):
        """ User Authentication to Login """
        
        data = api.payload
        user = UserModel.get_username(data.get("username"))

        if user.verify_password(data.get("password")):
            access_token = create_access_token(identity=user)
            refresh_token = create_refresh_token(identity=user)
        
        else:
            raise UnauthorizedError("Username or password are invalid!")
        
        return {
            "success": True,
            "data": {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        }, 200

@api.route("/token/revoke/access/")
@api.doc(parser=jwt_parser)
class RevokeAccessToken(Resource):

    @jwt_required
    def post(self):
        """ Revoke Access Token Operation """
        jti = get_raw_jwt()["jti"]
        blacklist = BlacklistedTokenModel.get(jti)
        if blacklist:
            return None, 204
        blacklist = BlacklistedTokenModel(token=jti)
        blacklist.save()
        return {
            "success": True,
            "message": "Access Token Already Revoked"
        }, 200

@api.route("/token/refresh/")
class TokenRefresh(Resource):

    @jwt_refresh_token_required
    @api.doc(parser=jwt_refresh_parser)
    def post(self):
        """ Get new Access Token with Refresh Token """
        current_user = get_jwt_identity()
        return {
            "success": True,
            "data": {
                "access_token": create_access_token(identity=current_user),
            }
        }, 200


@api.route("/token/revoke/refresh/")
@api.doc(parser=jwt_refresh_parser)
class RevokeRefreshToken(Resource):

    @jwt_refresh_token_required
    def post(self):
        """ Revoke Refresh Token Operation """
        jti = get_raw_jwt()["jti"]
        blacklist = BlacklistedTokenModel(token=jti)
        blacklist.save()
        return {
            "success": True,
            "message": "Refresh Token Already Revoked"
        }, 200