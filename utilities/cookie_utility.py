from flask import Request, Response
from services.user_service import get_user_from_auth_token
from services.role_service import get_role_by_id

# function to add cookie value
def add_cookie(response: Response, key: str, value: str):
    response.set_cookie(key=key, value=value)

# function to get cookie value
def _get_cookie_value(request: Request,key: str):
    return request.cookies.get(key=key)

# function to get auth tokens from cookies
def get_auth_token_from_cookies(request: Request):
    tokens = []
    for i in range(3):
        token_value = _get_cookie_value(request=request, key=f"token_{i}")
        print(f"token_{i}: {token_value}")
        if token_value is None:
            return None
        else:
            tokens.append(_get_cookie_value(request=request, key=f"token_{i}"))
    return ".".join(tokens)

# function to check if user is signed_in
def is_user_signed_in(request: Request):
    token = get_auth_token_from_cookies(request=request)
    if token is None:
        return False
    else:
        return get_user_from_auth_token(token) is not None

# function to get current user data
def get_current_user_data(request: Request):
    user = get_user_from_auth_token(get_auth_token_from_cookies(request=request))
    user_role = get_role_by_id(user.user_role)
    return {
        "user_id": user.user_id,
        "user_first_name": user.user_first_name,
        "user_role": user_role.role_name
    }

