import re

def register_validator(data) -> None:
    if not data or (
        data and (
            'email' not in data or\
            'password' not in data
        )
    ):
        raise Exception({
            'msg': 'Email and password are required.',
            'code': 422
        })

    if not __is_email_valid(data['email']):
        raise Exception({'msg': 'Valid email is required.', 'code': 400})

    if not __is_password_valid(data['password']):
        raise Exception({'msg': 'Valid password is required.', 'code': 400})

def login_validator(data) -> None:
    if not data or (
        data and (
            'email_or_username' not in data or\
            'password' not in data
        )
    ):
        raise Exception({
            'msg': 'Email/Username and password are required!',
            'code': 422
        })

    if len(data['email_or_username']) <= 5 or\
        not __is_password_valid(data['password']):
        raise Exception({'msg': 'Invalid credentials!', 'code': 400})

def revoke_tokens_validator(data) -> None:
    if not data or (
        data and 'tokens' not in data
    ) or (
        data and 'tokens' in data and len(data['tokens']) == 0
    ):
        raise Exception({
            'msg': 'Tokens are required.',
            'code': 422
        })

def __is_email_valid(email: str) -> bool:
    if re.fullmatch(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        email
    ):
        return True
    return False

def __is_password_valid(password: str) -> bool:
    return len(password) >= 6 and len(password) <= 20 and\
        any(char.isdigit() for char in password) and\
        any(char.isupper() for char in password) and\
        any(char.islower() for char in password)