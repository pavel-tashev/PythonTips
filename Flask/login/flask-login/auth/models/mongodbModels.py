import os
from pymongo import MongoClient
from bson.objectid import ObjectId

from flask_bcrypt import Bcrypt
from flask_login import UserMixin


db_path = os.environ.get('MONGODB_PATH')
db_name = str(os.environ.get('MONGODB_NAME'))
client = MongoClient(db_path)
db = client[db_name]
bcrypt = Bcrypt()

class User(UserMixin):
    def __init__(
        self,
        email: str,
        username: str,
        password: str,
        _id = None
    ) -> None:
        self._id = str(ObjectId()) if _id is None else str(_id)

        self.email = email
        self.username = username
        self.password = password

    def get_id(self):
        return self._id

    @classmethod
    def get_by_id(cls, user_id: str):
        user = db['user'].find_one({'_id': ObjectId(user_id)})
        if user is None:
            return None

        return cls(**user)

    @classmethod
    def register(cls, email: str, username: str, password: str):
        if cls.get_by_email(email) or cls.get_by_username(username):
            raise Exception('User already exists!')

        user = cls(
            email = email,
            username = username,
            password = bcrypt.generate_password_hash(password)
        )
        db['user'].insert_one(
            {
                '_id': ObjectId(user._id),
                'email': user.email,
                'username': user.username,
                'password': user.password
            }
        )

        return user

    @classmethod
    def get_by_email(cls, email: str):
        if email is None:
            return None

        user = db['user'].find_one({ 'email': email })
        if user is None:
            return None

        return cls(**user)

    @classmethod
    def get_by_username(cls, username: str):
        if username is None:
            return None

        user = db['user'].find_one({ 'username': username })
        if user is None:
            return None

        return cls(**user)

    @classmethod
    def get_verified(cls, email_or_username: str, password: str):
        verify_user = cls.get_by_email(email_or_username)
        if verify_user is None:
            verify_user = cls.get_by_username(email_or_username)
            if verify_user is None:
                raise Exception('User does not exists!')

        if bcrypt.check_password_hash(verify_user.password, password):
            return verify_user

        raise Exception('Invalid password!')
