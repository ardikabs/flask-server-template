from functools import wraps
from flask_jwt_extended import (
    get_jwt_claims, 
    verify_jwt_in_request
)
from server.app import jwt
from server.main.models import BlacklistedTokenModel

from .http_exceptions import *


def jwt_has_role(role):
    def decorator(func):
        @wraps(func)    
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt_claims()
            if role != claims["role"]:
                raise ForbiddenError("Your place not belong here, go away!")
            return func(*args, **kwargs)
        return decorated_function
    return decorator

def jwt_has_any_role(roles):
    def decorator(func):
        @wraps(func)    
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt_claims()
            if claims["role"] not in roles :
                raise ForbiddenError("Your place not belong here, go away!")
            return func(*args, **kwargs)
        return decorated_function
    return decorator