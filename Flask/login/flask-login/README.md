# Introduction
User authorization workflow that includes registering a new user, login, logout as well as accessing pages that require authorization.

For the purpose of this project we use:
- **Flask-Login** - provides user session management for Flask. It handles the common tasks of logging in, logging out, and remembering your users' sessions over extended periods of time. It will store the active user's ID in the Flask Session, and let you easily log them in and out.
- **Flask-Session** - is an extension for Flask that adds support for Server-side session to your application.
- **flask_sqlalchemy** OR *pymongo* - database used to store sessions and users.

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

Please note that we use pymongo version 3.11.0 because it still supports methods `update` and `insert` used by flask-session. Unfortunately for newer versions of pymongo these methods are not supported which causes issues using flask-session with MongoDB storage.

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
    {
        "email": "EMAIL_ADDRESS",
        "password": "PASSWORD"
    }
```

## Log in
```
POST '/v1/auth/login'
    {
        "email_or_username": "EMAIL_ADDRESS_OR_USERNAME",
        "password": "PASSWORD"
    }
```

## Log out
```
POST '/v1/auth/logout'
```

## Home page - no authorization is required
```
GET '/'
```

## Profile page - authorization is required
```
GET '/profile'
```

NOTE: _Please note that we don't have a method responsible for refreshing the session of the user because that's handled by Flask-Session. Every time we request an endpoint requiring the user being logged in, Flask-Session checks the session and prolongs its expiry date if it exists and if it's still not expired._