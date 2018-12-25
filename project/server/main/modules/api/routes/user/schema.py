
from marshmallow import post_dump, post_load

from server.app import ma
from server.main.models import UserModel, RoleModel
from sqlalchemy.exc import IntegrityError

from ...http_exceptions import *
  
class UserSchema(ma.ModelSchema):
    password = ma.Field(load_only=True)
    password_hash = ma.Field(allow_none=True)
    class Meta:
        model = UserModel
        dump_only = (
            UserModel.id.key,
            UserModel.created_at.key,
            UserModel.modified_at.key,
        )

    
    @post_load
    def make_instance(self, data):
        user = UserModel.get_username(data.get("username"))
        if user:
            raise UnprocessableError(UserModel.__modelname__, user.username)
        
        user = UserModel()
        user.username = data.get("username")
        user.password = data.get("password")
        user.first_name = data.get("first_name")
        user.last_name = data.get("last_name")
        user.role = RoleModel.get_default()
        user.new()
        return user
    

    def dump_response(self, model):
        data, err = self.dump(model)
        if err: raise InternalError(err)
        return {
            "success": True,
            "data": data
        }

    