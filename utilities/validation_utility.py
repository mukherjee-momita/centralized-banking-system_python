from constants.name_constant import Name
from errors.application_error import ApplicationError

from http import HTTPStatus

import re


def validate_name(name: str, name_type: Name):
    if name_type is Name.COUNTRY_NAME or \
            name_type is Name.STATE_NAME or \
            name_type is Name.CITY_NAME or \
            name_type is Name.BANK_NAME:
        if name is None:
            raise ApplicationError(HTTPStatus.BAD_REQUEST, f"a valid {name_type.value} is required")

        name = name.strip()
        if len(name) < 1:
            raise ApplicationError(HTTPStatus.BAD_REQUEST, f"{name_type.value} must have at least 1 alphabet")
        if len(name) > 30:
            raise ApplicationError(HTTPStatus.BAD_REQUEST, f"{name_type.value} can have maximum of 30 alphabets")

    if name_type is Name.ROLE_NAME:
        if name is None:
            raise ApplicationError(HTTPStatus.BAD_REQUEST, "a valid role name is required")

        name = name.strip()
        if len(name) < 1:
            raise ApplicationError(HTTPStatus.BAD_REQUEST, "role name must have at least 1 alphabet")
        if len(name) > 10:
            raise ApplicationError(HTTPStatus.BAD_REQUEST, "role name can have maximum of 10 alphabets")

    # if name is user's first name or last name
    if name_type is Name.USER_FIRST_NAME or name_type is Name.USER_LAST_NAME:
        if name is None:
            raise ApplicationError(HTTPStatus.BAD_REQUEST, f"a valid {name_type.value} is required")
        name = name.strip()
        if len(name) < 3:
            raise ApplicationError(HTTPStatus.BAD_REQUEST, f"{name_type.value} must have at least 3 alphabets")
        if len(name) > 20:
            raise ApplicationError(HTTPStatus.BAD_REQUEST,
                                   f"{name_type.value} can have maximum of 20 alphabets")

    # if name is user's last name
    if name_type is Name.USER_MIDDLE_NAME:
        if name is not None:
            name = name.strip()
            if len(name) < 3:
                raise ApplicationError(HTTPStatus.BAD_REQUEST,
                                       f"{name_type.value} must have at least 3 alphabets")
            if len(name) > 20:
                raise ApplicationError(HTTPStatus.BAD_REQUEST,
                                       f"{name_type.value} can have maximum of 20 alphabets")


def validate_uuid(uuid: str, prefix: str):
    if uuid is None:
        raise ApplicationError(HTTPStatus.BAD_REQUEST, "a valid uuid is required")

    uuid = uuid.strip()
    if not uuid.startswith(prefix):
        raise ApplicationError(HTTPStatus.BAD_REQUEST, f"invalid uuid: {uuid}")

    uuid = uuid[len(prefix):]
    if not re.compile("[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}").match(uuid):
        raise ApplicationError(HTTPStatus.BAD_REQUEST, f"invalid uuid: {uuid}")


def validate_email(email: str):
    if email is None:
        raise ApplicationError(HTTPStatus.BAD_REQUEST, "a valid email is required")
    email = email.strip()

    if not re.compile("[a-zA-Z0-9_\.\+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-\.]+").match(email):
        raise ApplicationError(HTTPStatus.BAD_REQUEST, "invalid email")


def validate_contact(contact: str):
    if contact is None:
        raise ApplicationError(HTTPStatus.BAD_REQUEST, "a valid contact number is required")
    contact = contact.strip()
    if not re.compile("^[0-9]{10}").match(contact):
        raise ApplicationError(HTTPStatus.BAD_REQUEST, "invalid contact number")


def validate_password(password: str):
    if password is None:
        raise ApplicationError(HTTPStatus.BAD_REQUEST, "a valid password is required")
    password = password.strip()
    if len(password) < 5:
        raise ApplicationError(HTTPStatus.BAD_REQUEST, "password should have at least 5 characters")
    if len(password) > 15:
        raise ApplicationError(HTTPStatus.BAD_REQUEST, "password can have maximum of 15 characters")


def validate_address(address_data: str, null_allowed: bool):
    if address_data is None and not null_allowed:
        raise ApplicationError(HTTPStatus.BAD_REQUEST, "invalid address data")