import uuid
from http import HTTPStatus

from services.city_service import get_city_by_city_id
from repositories.address_repository import AddressRepository
from utilities.database_utility import DatabaseUtility
from utilities.validation_utility import validate_address, validate_uuid
from schemas.database_schema import Address
from errors.application_error import ApplicationError


def _generate_address_id():
    # set address id prefix
    address_id_prefix = "addr_"

    # prepare first address id
    a_id = address_id_prefix+str(uuid.uuid4())

    # check if address id exists
    while AddressRepository.find_address_by_id(a_id, DatabaseUtility.get_session()) is not None:
        # prepare new address id
        a_id = address_id_prefix + str(uuid.uuid4())

    # return address id
    return a_id


# function to add a new address
def add_new_address(building_no: str, line: str, landmark: str, zip_code: str, city_id: str):
    # validate address
    validate_address(building_no, False)
    validate_address(line, False)
    validate_address(landmark, True)
    validate_address(zip_code, False)

    # fetch city by city id
    city = get_city_by_city_id(city_id)

    # create new address object
    new_address = Address(
        address_id=_generate_address_id(),
        address_building_no=building_no,
        address_line=line,
        address_zip_code=zip_code,
        address_landmark=landmark,
        address_city=city_id
    )

    # insert new address object
    AddressRepository.insert_new_address_record(new_address, DatabaseUtility.get_session())

    # return new address object
    return new_address


# function to fetch address by id
def get_address_by_id(address_id: str):
    # validate address id
    validate_uuid(address_id, "addr_")

    # fetch address by id
    address = AddressRepository.find_address_by_id(address_id, DatabaseUtility.get_session())

    # check if address exists with id
    if address is None:
        raise ApplicationError(HTTPStatus.NOT_FOUND, f"address not found with id: {address_id}")
    else:
        return address