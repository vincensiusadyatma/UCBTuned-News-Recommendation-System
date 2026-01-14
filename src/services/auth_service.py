from src.repositories import AuthRepository
from werkzeug.security import generate_password_hash, check_password_hash


class AuthService:
    def __init__(self):
        self.repo = AuthRepository()

    def register(self, username,password):
        hashedPW = generate_password_hash(password)
        self.repo.create_usser(username,hashedPW)
