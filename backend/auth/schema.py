from flask import request
from marshmallow import Schema, pre_load, post_load, fields, validate, validates
from marshmallow.exceptions import ValidationError
from werkzeug.security import generate_password_hash
import bleach


class AuthRegister(Schema):
    firstname = fields.String(
        required=True,
        error_messages={"required": "Firstname field is required."},
        validate=validate.Length(min=1, error="Firstname field cannot be empty."),
    )
    lastname = fields.String(
        required=True,
        error_messages={"required": "Lastname field is required."},
        validate=validate.Length(min=1, error="Lastname field cannot be empty."),
    )
    email = fields.Email(
        required=True,
        error_messages={
            "required": "Email field is required.",
            "invalid": "Email address is not valid.",
        },
    )

    phone_number = fields.String(
        required=True,
        error_messages={"required": "Phone number field is required."},
        validate=validate.Regexp(regex=r"^[0-9]{11}$", error="Invalid phone number."),
    )
    password = fields.String(
        required=True,
        error_messages={"required": "Password field is required."},
        validate=validate.Length(min=8, error="Password is too short."),
    )
    password_confirmation = fields.String(
        required=True,
        error_messages={"required": "Password confirmation field is required."},
    )

    @validates("password_confirmation")
    def confirm_password(self, value):
        if value != request.json.get("password"):
            raise ValidationError("Password confirmation does not match.")

    @pre_load
    def sanitize(self, data: dict, **kwargs):
        """
        Removes HTML Tags and trims each input value that are strings
        """
        data_copy = {
            k: (bleach.clean(v, strip=True).strip() if type(v) == str else v)
            for k, v in data.items()
        }

        return data_copy

    @post_load
    def finalize(self, data: dict, **kwargs):
        """
        Validates password_confirmation, removes it from data
        dictionary, hashes password and convert strings to
        lowercase
        """
        data_copy = {k: (v.lower() if type(v) == str else v) for k, v in data.items()}

        del data_copy["password_confirmation"]
        data_copy["password"] = generate_password_hash(data_copy["password"])
        return data_copy
