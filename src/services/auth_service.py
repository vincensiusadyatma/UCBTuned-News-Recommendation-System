from src.repositories import AuthRepository
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, timezone
import jwt
from src.config import Config

class AuthService:
    def __init__(self):
        self.repo = AuthRepository()

    def register(self, username,password):
        hashedPW = generate_password_hash(password)
        self.repo.create_usser(username,hashedPW)

    def authenticate(self,username,password):
        user = self.repo.get_user_by_username(username)

        if not user or not check_password_hash(user.password, password):
            raise ValueError("Invalid credentials")

        token = jwt.encode(
            {
                "user_id": user.id,
                "exp": datetime.now(timezone.utc) + timedelta(hours=1)
            },
             Config.KEY,
            algorithm="HS256"
        )

        return token
