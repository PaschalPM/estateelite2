import pytest
from core import app, db
import requests
from json import dumps
from users.model import User
from properties.model import Property, Image

REGISTER_URI = "http://localhost:5001/api/auth/register"


@pytest.fixture
def setup():
    with app.app_context():
        db.create_all()

    yield {
        "firstname": "John",
        "lastname": "Doe",
        "email": "johndoe@gmail.com",
        "phone_number": "07031109090",
        "password": "12345678",
        "password_confirmation": "12345678",
    }

    with app.app_context():
        db.drop_all()


def make_request(data):
    return requests.post(
        REGISTER_URI, data=dumps(data), headers={"Content-Type": "application/json"}
    )


def test_with_valid_payload_passed_twice(setup: dict):
    data = setup
    res = make_request(data)
    assert res.status_code == 200
    res_body = res.json()
    assert res_body.get("message") == "User created successfully."
    res = make_request(data)
    assert res.status_code == 400
    res_body = res.json()
    message = res_body.get("message")
    assert "phone_number" in message or "email" in message
    if message.get("phone_number"):
        assert message.get("phone_number")[0] == "Phone number already exists."
    if message.get("email"):
        assert message.get("email")[0] == "Email address already exists."


def generate_invalid_payload(
    data, key: str, test_value: str, expected_msg: str, expected_status=400
):
    data[key] = test_value
    res = make_request(data)
    assert res.status_code == expected_status
    err_msg = res.json().get("message")
    assert err_msg[key][0] == expected_msg


def test_with_invalid_payload(setup: dict):
    INVALID_EMAIL_ERR_MSG = "Email address is not valid."
    INVALID_PHONE_NUM_ERR_MSG = "Invalid phone number."
    data = setup.copy()
    generate_invalid_payload(
        data, "firstname", "  ", "Firstname field cannot be empty."
    )
    generate_invalid_payload(data, "lastname", "  ", "Lastname field cannot be empty.")
    generate_invalid_payload(data, "email", "  ", INVALID_EMAIL_ERR_MSG)
    generate_invalid_payload(data, "email", "joedoegmail.com", INVALID_EMAIL_ERR_MSG)
    generate_invalid_payload(data, "phone_number", "   ", INVALID_PHONE_NUM_ERR_MSG)
    generate_invalid_payload(
        data, "phone_number", "07031111120984757", INVALID_PHONE_NUM_ERR_MSG
    )
    generate_invalid_payload(
        data, "phone_number", "070311uyr12", INVALID_PHONE_NUM_ERR_MSG
    )
    generate_invalid_payload(data, "password", "1234567", "Password is too short.")
    generate_invalid_payload(
        data,
        "password_confirmation",
        "1234567asbc",
        "Password confirmation does not match.",
    )


def test_missing_fields(setup):
    for key in setup:
        data_copy = setup.copy()
        del data_copy[key]
        res = make_request(data_copy)
        assert res.status_code == 400
        if key == "phone_number":
            assert (
                res.json().get("message")[key][0] == "Phone number field is required."
            )
        elif key == "password_confirmation":
            assert (
                res.json().get("message")[key][0]
                == "Password confirmation field is required."
            )
        else:
            assert (
                res.json().get("message")[key][0]
                == f"{key.capitalize()} field is required."
            )
