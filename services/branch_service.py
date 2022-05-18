import json
import uuid
from http import HTTPStatus

from constants.name_constant import Name
from errors.application_error import ApplicationError
from repositories.branch_repository import BranchRepository
from schemas.database_schema import Branch
from services.address_service import add_new_address
from services.bank_service import get_bank_by_id
from utilities.database_utility import DatabaseUtility
from utilities.validation_utility import validate_name, validate_email, validate_contact, validate_uuid


# function to generate branch id
def _generate_branch_id():
    # set branch id prefix
    branch_id_prefix = "branch_"
    # prepare first branch id
    b_id = branch_id_prefix+str(uuid.uuid4())
    # check if branch id exists
    while BranchRepository.find_branch_by_id(b_id, DatabaseUtility.get_session()) is not None:
        # prepare new branch id
        b_id = branch_id_prefix + str(uuid.uuid4())
    # return branch id
    return b_id


def add_new_branch(branch_name: str, 
                   branch_email: str, 
                   branch_contact: str,
                   bank_id: str,
                   building_no: str,
                   line: str,
                   landmark: str,
                   zip_code: str,
                   city_id: str
                   ):
    # validate branch name, email and contact
    validate_name(branch_name, Name.BRANCH_NAME)
    validate_email(branch_email)
    validate_contact(branch_contact)

    # check if branch with same name exists for same bank with given id
    if BranchRepository.find_branch_by_branch_name_and_bank_id(
            branch_name, bank_id, DatabaseUtility.get_session()) is not None:
        raise ApplicationError(HTTPStatus.CONFLICT,
                               f"branch with same name: {branch_name} already exists for bank with id: "
                               f"{bank_id}")

    # check if branch with same email exists
    if BranchRepository.find_branch_by_email(branch_email, DatabaseUtility.get_session()) is not None:
        raise ApplicationError(HTTPStatus.CONFLICT,
                               f"branch with same email already exists: {branch_email}")

    # check if branch with same contact number exists
    if BranchRepository.find_branch_by_contact(branch_contact, DatabaseUtility.get_session()) is not None:
        raise ApplicationError(HTTPStatus.CONFLICT,
                               f"branch with same contact number already exists: {branch_contact}")

    # fetch bank data by bank id
    bank = get_bank_by_id(bank_id)

    # add branch address
    b_address = add_new_address(
        building_no=building_no,
        line=line,
        landmark=landmark,
        zip_code=zip_code,
        city_id=city_id
    )

    # create new branch object
    new_branch = Branch(
        branch_id=_generate_branch_id(),
        branch_name=branch_name,
        branch_email=branch_email,
        branch_contact=branch_contact,
        bank_id=bank_id,
        branch_address=b_address.address_id
    )

    # insert new branch object
    BranchRepository.insert_new_branch_record(new_branch, DatabaseUtility.get_session())

    # return new branch object
    return new_branch


def get_branch_by_branch_id(branch_id: str):
    # validate branch id
    validate_uuid(branch_id, "branch_")

    # fetch branch by id
    branch = BranchRepository.find_branch_by_id(branch_id, DatabaseUtility.get_session())

    # check if branch exists with given id
    if branch is None:
        raise ApplicationError(HTTPStatus.NOT_FOUND, f"branch with id not found: {branch_id}")
    else:
        return branch


def get_branches_by_bank_id(bank_id: str):
    # validate bank id
    validate_uuid(bank_id, "bank_")

    # fetch branches by bank id
    return BranchRepository.find_branch_by_bank_id(bank_id, DatabaseUtility.get_session())