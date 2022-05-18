from dotenv import load_dotenv
from os import environ
from http import HTTPStatus

from errors.application_error import ApplicationError

class EnvironmentUtility:

    @classmethod
    def initialize_environment_utility(cls):
        load_dotenv()
    
    @classmethod
    def get_environment_variable_value(cls, key: str):
        # fetch value from environment
        value = environ.get(key)
        if value is None:
            # raise exception if value is not available
            raise ApplicationError(HTTPStatus.INTERNAL_SERVER_ERROR, 
                                    f"invalid environment variable: {key}")
        else:
            # return environment variable value
            return value