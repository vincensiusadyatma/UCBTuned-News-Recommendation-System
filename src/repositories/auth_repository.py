from src.config import Session
from src.models.User import User
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

class AuthRepository:

    def get_user_by_username(self, username: str):
        session = Session()
        try:
            return session.query(User).filter(User.username == username).first()

        except SQLAlchemyError as e:
            session.rollback()
            raise e

        finally:
            session.close()


    def get_user_by_id(self, user_id: int):
        session = Session()
        try:
            return (
                session.query(User)
                .options(joinedload(User.role))  # 🔥 penting
                .filter(User.id == user_id)
                .first()
            )
        finally:
            session.close()


    def get_users_paginated(self, page: int = 1, per_page: int = 20):
        session = Session()
        try:
            offset = (page - 1) * per_page

            users = (
                session.query(User)
                .order_by(User.id)
                .offset(offset)
                .limit(per_page)
                .all()
            )

            total = session.query(User).count()

            return users, total

        except SQLAlchemyError as e:
            session.rollback()
            raise e

        finally:
            session.close()


    def create_user(self, username: str, hashed_password: str):
        session = Session()
        try:
            user = User(username=username, password=hashed_password,role_id=2)
            session.add(user)
            session.commit()
            session.refresh(user)

            return user

        except SQLAlchemyError as e:
            session.rollback()  
            raise e

        finally:
            session.close()