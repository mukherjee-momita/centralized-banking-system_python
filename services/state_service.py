import json
import uuid
from http import HTTPStatus

from repositories.state_repository import StateRepository
from utilities.database_utility import DatabaseUtility
from utilities.validation_utility import validate_name, validate_uuid
from constants.name_constant import Name
from services.country_service import get_country_by_id
from errors.application_error import ApplicationError
from schemas.database_schema import State


# function to generate state id
def _generate_state_id():
    # set state id prefix
    state_id_prefix = "state_"

    # prepare first state id
    s_id = state_id_prefix+str(uuid.uuid4())

    # check if state id exists
    while StateRepository.find_state_by_id(s_id, DatabaseUtility.get_session()) is not None:
        # prepare new state id
        s_id = state_id_prefix + str(uuid.uuid4())

    # return state id
    return s_id


# function to add a new state
def add_new_state(state_name: str, country_id: str):
    # validate state name
    validate_name(state_name, Name.STATE_NAME)

    # fetch country for state
    country = get_country_by_id(country_id)

    # check if state with same name for same country already exists
    if StateRepository.find_state_by_country_id_and_state_name(country.country_id,
                                                               state_name,
                                                               DatabaseUtility.get_session()) is not None:
        raise ApplicationError(HTTPStatus.CONFLICT,
                               f"state with name: {state_name} already exists for country: {country.country_name}")

    # create new state object
    new_state = State(
        state_id=_generate_state_id(),
        state_name=state_name,
        country_id=country.country_id
    )

    # insert new state object
    StateRepository.insert_new_state_record(new_state, DatabaseUtility.get_session())

    # return new state object
    return new_state


# function to find states by country id
def get_states_by_country_id(country_id: str):
    # validate country id
    validate_uuid(country_id, "country_")

    # fetch states for country
    return StateRepository.find_states_by_country_id(country_id, DatabaseUtility.get_session())


# function to find state by id and country id
def get_state_by_id_and_country_id(state_id: str, country_id: str):
    # validate state id and country id
    validate_uuid(state_id, "state_")
    validate_uuid(country_id, "country_")

    # fetch state by id and country id
    state = StateRepository.find_state_by_country_id_and_state_id(country_id, state_id, DatabaseUtility.get_session())

    # check if state found
    if state is None:
        raise ApplicationError(HTTPStatus.NOT_FOUND,
                               f"no state found with id: {state_id} and country id: {country_id}")
    else:
        return state


# function to get state by id
def get_state_by_id(state_id: str):
    # validate state id
    validate_uuid(state_id, "state_")

    # fetch state by id
    state = StateRepository.find_state_by_id(state_id, DatabaseUtility.get_session())

    # check if state exists
    if state is None:
        raise ApplicationError(HTTPStatus.NOT_FOUND, f"state with id not found: {state_id}")
    else:
        return state

# function to get all states
def get_all_states():
    return StateRepository.find_all_states(DatabaseUtility.get_session())