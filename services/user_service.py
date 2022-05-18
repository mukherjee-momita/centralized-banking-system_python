from utilities.validation_utility import validate_name, validate_email, validate_contact, validate_password, validate_uuid
from utilities.database_utility import DatabaseUtility
from utilities.environment_utility import EnvironmentUtility
from constants.name_constant import Name
from constants.role_constant import Role
from repositories.user_repository import UserRepository
from schemas.database_schema import User
from services.role_service import get_role_by_name, get_role_by_id
from errors.application_error import ApplicationError

import uuid
from bcrypt import hashpw, gensalt, checkpw
from jwt import encode, decode
from http import HTTPStatus

# function to generate json web token
def generate_jwt(payload: dict):
    jwt_key = EnvironmentUtility.get_environment_variable_value("jwt_key")
    jwt_algorithm = EnvironmentUtility.get_environment_variable_value("jwt_algorithm")
    return encode(payload=payload, key=jwt_key, algorithm=jwt_algorithm)

# function to decode json web token
def decode_jwt(token: str):
    jwt_key = EnvironmentUtility.get_environment_variable_value("jwt_key")
    jwt_algorithm = EnvironmentUtility.get_environment_variable_value("jwt_algorithm")
    print(f"token: {token}")
    return decode(jwt=token, key=jwt_key, algorithms=jwt_algorithm)

# function to generate user id
def _generate_user_id():
    # set user id prefix
    user_id_prefix = "user_"

    # prepare first user id
    u_id = user_id_prefix+str(uuid.uuid4())

    # check if user id exists
    while UserRepository.find_user_by_id(u_id, DatabaseUtility.get_session()) is not None:
        # prepare new user id
        u_id = user_id_prefix + str(uuid.uuid4())

    # return user id
    return u_id

# function to get user id from auth token
def get_user_from_auth_token(auth_token: str):
    payload = decode_jwt(token=auth_token)
    if payload["user_id"] is None:
        return None
    else:
        return UserRepository.find_user_by_id(payload["user_id"], 
                            DatabaseUtility.get_session())

# function to encrypt password
def encrypt_password(plain_password: str):
    return hashpw(password=plain_password, salt=gensalt(rounds=12))

# function to register a user
def register_user(first_name: str, middle_name: str, last_name: str, email: str, contact: str, password: str):
    # validate user email and contact
    validate_email(email)
    validate_contact(contact)

    # check if user with same email exists
    if UserRepository.find_user_by_email(email, DatabaseUtility.get_session()) is not None:
        raise ApplicationError(HTTPStatus.CONFLICT, "user with same email already exists")

    # check if user with same contact exists
    if UserRepository.find_user_by_contact(contact, DatabaseUtility.get_session()) is not None:
        raise ApplicationError(HTTPStatus.CONFLICT, "user with same contact already exists")

    # validate rest of the user details
    validate_name(first_name, Name.USER_FIRST_NAME)
    validate_name(middle_name, Name.USER_MIDDLE_NAME)
    validate_name(last_name, Name.USER_LAST_NAME)
    validate_password(password)

    # fetch user role
    role = get_role_by_name("USER")

    # create user object
    new_user = User(
        user_id=_generate_user_id(),
        user_first_name=first_name,
        user_middle_name=middle_name,
        user_last_name=last_name,
        user_email=email,
        user_contact=contact,
        user_enabled=True,
        user_password=encrypt_password(password.encode("utf-8")),
        user_role=role.role_id
    )

    # save new user
    UserRepository.insert_new_user(new_user, DatabaseUtility.get_session())

    # return new user
    return new_user

# function to login a user
def login_user(email: str, password: str):
    # validate user email and password
    validate_email(email=email)
    validate_password(password=password)

    # fetch user data
    user = UserRepository.find_user_by_email(email=email, session=DatabaseUtility.get_session())

    # check if user exists
    if user is None:
        raise ApplicationError(HTTPStatus.NOT_FOUND, "user with email not found")
    
    else:
        # check if user is enabled
        if user.user_enabled:
            # check user password
            if checkpw(password.encode("utf-8"), user.user_password):
                
                # create jwt payload
                payload = {
                    "user_id": user.user_id
                }

                # create jwt
                auth_token = generate_jwt(payload=payload)

                # return auth token
                return auth_token
            else:
                raise ApplicationError(HTTPStatus.UNAUTHORIZED, "incorrect password")
        else:
            raise ApplicationError(HTTPStatus.FORBIDDEN, "user is not allowed to sign in")

# function to view all users
def view_all_users():
    return UserRepository.find_all_users(DatabaseUtility.get_session())

# function to get user by id
def get_user_by_id(u_id: str):
    # validate uuid
    validate_uuid(u_id, "user_")

    # fetch user by id
    user = UserRepository.find_user_by_id(u_id, DatabaseUtility.get_session())

    # check if user exists with id
    if user is None:
        raise ApplicationError(HTTPStatus.NOT_FOUND, f"user not found with id: {u_id}")
    else:
        return user
