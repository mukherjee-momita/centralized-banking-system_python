import uuid
import json
from http import HTTPStatus

from repositories.country_repository import CountryRepository
from utilities.database_utility import DatabaseUtility
from utilities.validation_utility import validate_uuid, validate_name
from constants.name_constant import Name
from errors.application_error import ApplicationError
from schemas.database_schema import Country

# function to generate country id
def _generate_country_id():
    # set country id prefix
    country_id_prefix = "country_"

    # prepare first country id
    c_id = country_id_prefix+str(uuid.uuid4())

    # check if country id exists
    while CountryRepository.find_country_by_id(c_id, DatabaseUtility.get_session()) is not None:
        # prepare new country id
        c_id = country_id_prefix + str(uuid.uuid4())

    # return country id
    return c_id


# function to add a new country
def add_new_country(country_name: str):
    # validate country name
    validate_name(country_name, Name.COUNTRY_NAME)

    # check for existing country with same name
    if CountryRepository.find_country_by_name(country_name, DatabaseUtility.get_session()) is not None:
        raise ApplicationError(HTTPStatus.CONFLICT, f"a country with same name already exists: {country_name}")

    # create new country object
    new_country = Country(
        country_id=_generate_country_id(),
        country_name=country_name
    )

    # insert new country object
    CountryRepository.insert_new_country(new_country, DatabaseUtility.get_session())

    # return new country object
    return new_country


# function to find country by id
def get_country_by_id(c_id: str):
    # validate country id
    validate_uuid(c_id, "country_")

    # fetch country by id
    country = CountryRepository.find_country_by_id(c_id, DatabaseUtility.get_session())

    # check if country exists with given id
    if country is None:
        raise ApplicationError(HTTPStatus.NOT_FOUND, f"country with id not found: {c_id}")
    else:
        return country


# function to find country by name
def get_country_by_name(c_name: str):
    # validate country name
    validate_name(c_name, Name.COUNTRY_NAME)

    # fetch country by name
    country = CountryRepository.find_country_by_name(c_name, DatabaseUtility.get_session())

    # check if country exists with given name
    if country is None:
        raise ApplicationError(HTTPStatus.NOT_FOUND, f"country with name not found: {c_name}")
    else:
        return country


# function to get all countries
def get_all_countries():
    # return all country data from database
    return CountryRepository.find_all_countries(DatabaseUtility.get_session())
