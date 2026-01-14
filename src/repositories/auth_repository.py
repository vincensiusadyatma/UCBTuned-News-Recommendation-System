from src.config import Session
from src.models.User import User

class AuthRepository:
    def __init__(self):
        self.session = Session()

    def get_user_by_username(self, username:str):
        return self.session.query(User).filter(User.username == username).first()
    
    def create_usser(self, username: str, hashed_password: str):
        user = User(username=username, password=hashed_password)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user