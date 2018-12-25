
from flask_restplus import fields
from . import api

user_field = api.model("User", {
    "id": fields.Integer(readonly=True, description="User ID"),
    "username": fields.String(required=True, description="User Name"),
    "password": fields.String(required=True, description="User Password"),
    "first_name": fields.String(required=True, description="User First Name"),
    "last_name": fields.String(required=True, description="User Last Name"),
    "created_at": fields.DateTime(readonly=True, description="Created Timestamp"),
    "modified_at": fields.DateTime(readonly=True, description="Modified Timestamp")
})

user_response = api.model("ResponseUser", {
    "success": fields.Boolean(description="Response Success Flag"),
    "data": fields.Nested(user_field,skip_none=True)
})