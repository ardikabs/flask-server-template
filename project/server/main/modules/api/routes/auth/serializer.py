
from flask_restplus import fields
from . import api

user_login_field = api.model("UserLogin", {
    "username": fields.String(required=True, description="User Name"),
    "password": fields.String(required=True, description="User Password")
})

login_response = api.model("ResponseLogin", {
    "success": fields.Boolean(description="Response Success Flag"),
    "data": fields.Nested(
        api.model("Token", {
            "access_token": fields.String(description="Access Token"),
            "refresh_token": fields.String(description="Refresh Token")
        })
    ,skip_none=True)
})