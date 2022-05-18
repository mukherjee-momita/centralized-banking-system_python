import json
import uuid
from http import HTTPStatus

from repositories.city_repository import CityRepository
from utilities.database_utility import DatabaseUtility
from utilities.validation_utility import validate_name, validate_uuid
from constants.name_constant import Name
from services.state_service import get_state_by_id
from errors.application_error import ApplicationError
from schemas.database_schema import City


# function to generate city_data id
def _generate_city_id():
    # set city_data id prefix
    city_id_prefix = "city_"

    # prepare first city_data id
    c_id = city_id_prefix+str(uuid.uuid4())

    # check if city_data id exists
    while CityRepository.find_city_by_id(c_id, DatabaseUtility.get_session()) is not None:
        # prepare new city_data id
        c_id = city_id_prefix + str(uuid.uuid4())

    # return city_data id
    return c_id


# function to add a new city
def add_new_city(city_name: str, state_id: str):
    # validate city_data name
    validate_name(city_name, Name.CITY_NAME)

    # validate state id
    state = get_state_by_id(state_id)

    # check if city_data with same name and same state id exists
    if CityRepository.find_city_by_city_name_and_state_id(
            city_name, state_id, DatabaseUtility.get_session()) is not None:
        raise ApplicationError(HTTPStatus.CONFLICT,
                               f"a city with same name: {city_name} already exists for state with id: {state_id}")

    # create new city_data object
    new_city = City(
        city_id=_generate_city_id(),
        city_name=city_name,
        state_id=state_id
    )

    # insert new city_data record
    CityRepository.insert_new_city(new_city, DatabaseUtility.get_session())

    # return new city_data record
    return new_city


# function to get cities by state id
def get_cities_by_state_id(state_id: str):
    # validate state id
    validate_uuid(state_id, "state_")

    # fetch cities by state id
    cities = CityRepository.find_cities_by_state_id(state_id, DatabaseUtility.get_session())

    # return result list
    return cities


# function to get city by city id
def get_city_by_city_id(city_id: str):
    # validate city id
    validate_uuid(city_id, "city_")

    # fetch city by id
    city = CityRepository.find_city_by_id(city_id, DatabaseUtility.get_session())

    # check if city exists with given id
    if city is None:
        raise ApplicationError(HTTPStatus.NOT_FOUND, f"city with id not found: {city_id}")
    else:
        return city


# function to get all cities
def get_all_cities():
    return CityRepository.find_all_cities(DatabaseUtility.get_session())
