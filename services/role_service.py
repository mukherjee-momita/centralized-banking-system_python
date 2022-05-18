from repositories.role_repository import RoleRepository
from utilities.database_utility import DatabaseUtility
from utilities.validation_utility import validate_name, validate_uuid
from constants.name_constant import Name
from errors.application_error import ApplicationError
from schemas.database_schema import Role
from http import HTTPStatus

import uuid

# function to generate role id
def _generate_role_id():
    # set role id prefix
    role_id_prefix = "role_"

    # prepare first role id
    r_id = role_id_prefix+str(uuid.uuid4())

    # check if role id exists
    while RoleRepository.get_role_by_id(r_id, DatabaseUtility.get_session()) is not None:
        # prepare new role id
        r_id = role_id_prefix + str(uuid.uuid4())

    # return role id
    return r_id

# function to add a new role record
def add_new_role(role_name: str):
    # validate role name
    validate_name(role_name, Name.ROLE_NAME)

    # check for existing role with same name
    if RoleRepository.get_role_by_name(role_name, DatabaseUtility.get_session()) is not None:
        raise ApplicationError(HTTPStatus.CONFLICT, f"role with same name already exists: {role_name}")

    # generate role object
    new_role = Role(
        role_id=_generate_role_id(),
        role_name=role_name
    )

    # insert new role
    RoleRepository.add_new_role(new_role, DatabaseUtility.get_session())

    # return role object
    return new_role

# function to get role by name
def get_role_by_name(role_name: str):
    # validate role name
    validate_name(role_name, Name.ROLE_NAME)

    # fetch role by name
    role = RoleRepository.get_role_by_name(role_name, DatabaseUtility.get_session())

    # check if role exists
    if role is None:
        raise ApplicationError(HTTPStatus.NOT_FOUND, f"role with name not found: {role_name}")
    else:
        return role

# function to get role by id
def get_role_by_id(role_id: str):
    # validate role id
    validate_uuid(role_id, "role_")

    # fetch role by id
    role = RoleRepository.get_role_by_id(role_id, DatabaseUtility.get_session())

    # check if role exists
    if role is None:
        raise ApplicationError(HTTPStatus.NOT_FOUND, f"role with id not found: {role_id}")
    else:
        return role
