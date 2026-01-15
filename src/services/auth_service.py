from src.repositories import AuthRepository
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, timezone
import jwt
from src.config import Config
from flask import request
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
    
    def get_curent_user(self):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        try:
            token = auth_header.split(" ")[1]  # Bearer <token>
            payload = jwt.decode(
                token,
                Config.KEY,
                algorithms=["HS256"]
            )
            return payload  # isinya data user
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
