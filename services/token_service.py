import datetime
import json
import uuid

from repositories.token_repository import TokenRepository
from schemas.database_schema import Token
from services.bank_service import get_bank_by_id
from services.branch_service import get_branch_by_branch_id
from services.user_service import get_user_by_id


# function to generate token id
from utilities.database_utility import DatabaseUtility
from utilities.validation_utility import validate_uuid


def _generate_token_id():
    # set token id prefix
    token_id_prefix = "token_"
    # prepare first token id
    t_id = token_id_prefix+str(uuid.uuid4())
    # check if token id exists
    while TokenRepository.find_token_by_id(t_id, DatabaseUtility.get_session()) is not None:
        # prepare new token id
        t_id = token_id_prefix + str(uuid.uuid4())
    # return token id
    return t_id


def add_new_token(token_bank_id: str, token_branch_id: str, token_date: str, user_id: str):
    # fetch bank data
    bank = get_bank_by_id(token_bank_id)

    # fetch branch data
    branch = get_branch_by_branch_id(token_branch_id)

    # fetch user data
    user = get_user_by_id(user_id)

    # create new token
    new_token = Token(
        token_id=_generate_token_id(),
        token_created_on=datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        token_bank_id=token_bank_id,
        token_branch_id=token_branch_id,
        token_date=token_date,
        token_user_id=user_id
    )

    # insert new token record
    TokenRepository.insert_new_token_record(new_token, DatabaseUtility.get_session())

    # return new token
    return new_token


def get_tokens_by_user_id(user_id: str):
    # validate user id
    validate_uuid(user_id, "user_")

    # fetch tokens by user id
    return TokenRepository.find_token_by_user_id(user_id, DatabaseUtility.get_session())
