from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import String, Column, Integer

from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
bcrypt = Bcrypt()

class User(UserMixin, db.Model):
    id = Column(Integer, primary_key = True)

    email = Column(String(250), nullable = False, unique = True)
    username = Column(String(250), nullable = False, unique = True)
    password = Column(String(250), unique = False)

    @classmethod
    def get_by_id(cls, user_id: int):
        return cls.query.get(user_id)

    @classmethod
    def register(cls, email: str, username: str, password: str):
        if cls.get_by_email(email) or cls.get_by_username(username):
            raise Exception('User already exists!')

        try:
            user = cls(
                email = email,
                username = username,
                password = bcrypt.generate_password_hash(password)
            )
            db.session.add(user)
            db.session.commit()

            return user
        except NoResultFound:
            raise Exception('SQLAlchemy error!')

    @classmethod
    def get_by_email(cls, email: str):
        if email is None:
            return None

        try:
            query = cls.query.filter_by(email = email)
            user = query.one()
        except NoResultFound:
            return None

        return user

    @classmethod
    def get_by_username(cls, username: str):
        if username is None:
            return None

        try:
            query = cls.query.filter_by(username = username)
            user = query.one()
        except NoResultFound:
            return None

        return user

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
