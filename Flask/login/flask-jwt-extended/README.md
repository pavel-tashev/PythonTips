# Introduction
User authorization workflow that includes registering a new user, login, logout, token refresh, revoking tokens as well as accessing pages that require authorization.

For the purpose of this project we use:
- **Flask-JWT-Extended** - for managing the user authorization workflow.
- **flask_sqlalchemy** OR **pymongo** - database used to store sessions and users.

# Configuration
Copy `.env.example` and create a new file `.env`. Inside the file set all required values.

Open files `app.py` and `auth/appAuth.py`. Depending on if you use SQLAlchemy or MongoDB comment/uncomment the corresponding lines of code in order to switch to the desired database.

## How to get a good secret key?
Open the Terminal and type:
```
python3
```

followed by:

```
import uuid
uuid.uuid4().hex

```

or

```
import secrets
secrets.token_urlsafe(12)
```

Get the generated key and set the value of `SECRET_KEY` in `.env` file .


# Installation
Create and activate a virtualenv and install the dependencies:
```
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```

If you use SQLAlchemy also run:
```
python3 install.py
```

# Run
```
source env/bin/activate
python3 app.py
```

# Stop
On Mac press Control + C and after that deactivate the virtual environment via:
```
deactivate
```

# Check the database
## SQLalchemy
In the Terminal type:
```
sqlite3 database.db
.tables
```

To get all records inside table user:
```
select * from user;
```

To exit the database console:
```
.exit
```

## MongoDB
Install Mongo Compass (url: https://www.mongodb.com/docs/compass/current/install/), open it and connect to localhost.

# Endpoints
## Register a new user
```
POST '/v1/auth/register'
    --header 'Authorization: Bearer TOKEN'
    --data-raw '{
        "email": "EMAIL_ADDRESS",
        "password": "PASSWORD"
    }'
```

## Log in
```
POST '/v1/auth/login'
    --header 'Authorization: Bearer TOKEN'
    --header 'Content-Type: application/json'
    --data-raw '{
        "email_or_username": "EMAIL_OR_USERNAME",
        "password": "PASSWORD"
    }'
```

## Log out
```
POST '/v1/auth/logout'
    --header 'Authorization: Bearer TOKEN'
```

## Refresh token
```
POST '/v1/auth/refresh'
    --header 'Authorization: Bearer TOKEN'
```

## Revoke a list of tokens
```
DELETE '/v1/auth/revoke-tokens'
    --header 'Authorization: Bearer TOKEN'
    --header 'Content-Type: application/json'
    --data-raw '{
        "tokens": [
            "TOKEN 1",
            "TOKEN 2",
            ...,
            "TOKEN N"
        ]
    }'
```

## Home page - no authorization is required
```
GET '/'
```

## Profile page - authorization is required
```
GET '/profile'
    --header 'Authorization: Bearer TOKEN'
```