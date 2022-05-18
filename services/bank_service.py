import json
import uuid
from http import HTTPStatus

from services import address_service as address_service
from repositories.bank_repository import BankRepository
from utilities.database_utility import DatabaseUtility
from utilities.validation_utility import validate_name, validate_email, validate_uuid
from constants.name_constant import Name
from errors.application_error import ApplicationError
from schemas.database_schema import Bank


# function to generate bank id
def _generate_bank_id():
    # set bank id prefix
    bank_id_prefix = "bank_"
    # prepare first bank id
    b_id = bank_id_prefix+str(uuid.uuid4())
    # check if bank id exists
    while BankRepository.find_bank_by_id(b_id, DatabaseUtility.get_session()) is not None:
        # prepare new bank id
        b_id = bank_id_prefix + str(uuid.uuid4())
    # return bank id
    return b_id


# function to add a new bank
def add_new_bank(bank_name: str, 
                bank_email: str,
                bank_address_building_no: str,
                bank_address_line: str,
                bank_address_zip: str,
                bank_address_landmark: str,
                bank_address_city_id: str):
    # validate bank name and email
    validate_name(bank_name, Name.BANK_NAME)
    validate_email(bank_email)

    # check if bank with same name exists
    if BankRepository.find_bank_by_name(bank_name, DatabaseUtility.get_session()) is not None:
        raise ApplicationError(HTTPStatus.CONFLICT, f"bank with same name already exists: {bank_name}")

    # check if bank with same email exists
    if BankRepository.find_bank_by_email(bank_email, DatabaseUtility.get_session()) is not None:
        raise ApplicationError(HTTPStatus.CONFLICT, f"bank with same email already exists: {bank_email}")

    # add bank address
    b_address = address_service.add_new_address(
        building_no=bank_address_building_no,
        line=bank_address_line,
        zip_code=bank_address_zip,
        landmark=bank_address_landmark,
        city_id=bank_address_city_id
    )

    # create new bank object
    new_bank = Bank(
        bank_id=_generate_bank_id(),
        bank_name=bank_name,
        bank_email=bank_email,
        bank_address=b_address.address_id
    )

    # insert new bank object
    BankRepository.insert_new_bank_record(new_bank, DatabaseUtility.get_session())

    # return new bank object
    return new_bank


def get_bank_by_id(bank_id: str):
    # validate bank id
    validate_uuid(bank_id, "bank_")

    # fetch bank by id
    bank = BankRepository.find_bank_by_id(bank_id, DatabaseUtility.get_session())

    # check if bank with id exists
    if bank is None:
        raise ApplicationError(HTTPStatus.NOT_FOUND, f"bank with id not found: {bank_id}")
    else:
        return bank


def get_all_banks():
    # fetch all banks data from database
    return BankRepository.find_all_banks(DatabaseUtility.get_session())
