import os
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId

from flask_bcrypt import Bcrypt


db_path = os.environ.get('MONGODB_PATH')
db_name = str(os.environ.get('MONGODB_NAME'))
client = MongoClient(db_path)
db = client[db_name]
bcrypt = Bcrypt()

class User():
    def __init__(
        self,
        email: str,
        username: str,
        password: str, _id = None
    ) -> None:
        self._id = str(ObjectId()) if _id is None else str(_id)
        self.id = self._id

        self.email = email
        self.username = username
        self.password = password

    def get_id(self) -> str:
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

    @classmethod
    def get_sessions(cls, user_id: str) -> list:
        return Session.get_user_sessions(user_id)

class Session():
    def __init__(
        self,
        user_id: str,
        jti_access: str,
        jti_refresh: str,
        _id = None,
        created_at = None
    ) -> None:
        self._id = str(ObjectId()) if _id is None else str(_id)
        self.user_id = user_id

        self.jti_access = jti_access
        self.jti_refresh = jti_refresh

        self.created_at = datetime.now() if created_at is None else created_at

    @classmethod
    def add(cls, user_id: str, jti_access: str, jti_refresh: str) -> None:
        session = cls(
            user_id = user_id,
            jti_access = jti_access,
            jti_refresh = jti_refresh
        )
        db['session'].insert_one(
            {
                '_id': ObjectId(session._id),
                'user_id': session.user_id,
                'jti_access': session.jti_access,
                'jti_refresh': session.jti_refresh,
                'created_at': session.created_at
            }
        )

    @classmethod
    def get_by_jti_access(cls, jti_access: str):
        if jti_access is None:
            return None

        session = db['session'].find_one({ 'jti_access': jti_access })
        if session is None:
            return None

        return cls(**session)

    @classmethod
    def get_by_jti_refresh(cls, jti_refresh: str):
        if jti_refresh is None:
            return None

        session = db['session'].find_one({ 'jti_refresh': jti_refresh })
        if session is None:
            return None

        return cls(**session)

    @classmethod
    def refresh(
        cls,
        jti_refresh: str,
        jti_access_new: str,
        jti_refresh_new: str
    ) -> None:
        db['session'].update_one(
            {
                'jti_refresh': jti_refresh
            },
            {
                "$set": {
                    'jti_access': jti_access_new,
                    'jti_refresh': jti_refresh_new
                }
            }
        )

    @classmethod
    def delete(cls, user_id: str, jti_access: str) -> None:
        db['session'].delete_one(
            {
                'jti_access': jti_access,
                'user_id': user_id
            }
        )

    @classmethod
    def get_user_sessions(cls, user_id: str) -> list:
        sessions = db['session'].find({ "user_id": user_id })
        return [
            cls(**session)
            for session in sessions
        ]
