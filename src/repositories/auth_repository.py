from src.config import Session
from src.models.User import User

class AuthRepository:
    def __init__(self):
        self.session = Session()

    def get_user_by_username(self, username:str):
        return self.session.query(User).filter(User.username == username).first()
    
    def get_user_by_id(self, user_id: int):
        return self.session.query(User).filter(User.id == user_id).first()
    
    def get_users_paginated(self, page: int = 1, per_page: int = 20):
        offset = (page - 1) * per_page

        users = (
            self.session.query(User)
            .order_by(User.id)
            .offset(offset)
            .limit(per_page)
            .all()
        )

        total = self.session.query(User).count()

        return users, total

    def create_user(self, username: str, hashed_password: str):
        user = User(username=username, password=hashed_password)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user