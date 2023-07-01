from flask import request, abort
from core.manage.storage import create
from core.manage.api_success_response import respond_with
from users.model import User
from auth.schema import AuthRegister
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError
from flasgger.utils import swag_from


@swag_from('/auth/swagger/register.yaml')
def register():
    data = request.get_json()

    try:
        auth_register_schema = AuthRegister()
        valid_data = auth_register_schema.load(data)
        create(User, valid_data)
        return respond_with("User created successfully.", status=201)
    except ValidationError as e:
        abort(400, description=e.messages)
    except IntegrityError as e:
        err_msg = {}
        if data.get("email") in str(e._message):
            err_msg["email"] = ["Email address already exists."]
        elif data.get("phone_number") in str(e._message):
            err_msg["phone_number"] = ["Phone number already exists."]
        abort(400, description=err_msg)
