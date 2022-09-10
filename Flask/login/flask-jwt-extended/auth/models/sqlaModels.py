from datetime import datetime
from dotenv import load_dotenv

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import (
    String,
    Column,
    Integer,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import declared_attr


load_dotenv()
db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
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

    @classmethod
    def get_sessions(cls, user_id: int) -> list:
        return Session.get_user_sessions(user_id)


class Session(db.Model):
    @declared_attr
    def __tablename__(cls):
        return 'session'

    id = Column(Integer, primary_key = True)
    user = db.relationship(User)
    user_id = Column(Integer, ForeignKey(User.id))

    jti_access = Column(String(36), nullable = False, index = True)
    jti_refresh = Column(String(36), nullable = False, index = True)

    created_at = Column(DateTime, default = datetime.now(), nullable = False)

    @classmethod
    def add(cls, user_id: int, jti_access: str, jti_refresh: str) -> None:
        session = cls(
            user_id = user_id,
            jti_access = jti_access,
            jti_refresh = jti_refresh
        )

        db.session.add(session)
        db.session.commit()

    @classmethod
    def get_by_jti_access(cls, jti_access: str):
        return cls.query.filter_by(jti_access = jti_access).scalar()

    @classmethod
    def get_by_jti_refresh(cls, jti_refresh: str):
        return cls.query.filter_by(jti_refresh = jti_refresh).scalar()

    @classmethod
    def refresh(
        cls,
        jti_refresh: str,
        jti_access_new: str,
        jti_refresh_new: str
    ) -> None:
        try:
            cls.query.filter_by(jti_refresh = jti_refresh).update(
                dict(
                    jti_access = jti_access_new,
                    jti_refresh = jti_refresh_new
                )
            )

            db.session.commit()
        except NoResultFound:
            pass

    @classmethod
    def delete(cls, user_id: int, jti_access: str) -> None:
        try:
            query = cls.query.filter_by(
                jti_access = jti_access,
                user_id = user_id
            )
            session = query.one()

            db.session.delete(session)
            db.session.commit()
        except NoResultFound:
            pass

    @classmethod
    def get_user_sessions(cls, user_id: int) -> list:
        return cls.query.filter_by(user_id = user_id).all()
