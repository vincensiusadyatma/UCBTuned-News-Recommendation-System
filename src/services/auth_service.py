from src.repositories import AuthRepository
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, timezone
import jwt
from src.config import Config
from flask import request

class AuthService:
    def __init__(self):
        self.repo = AuthRepository()

    def register(self, username,password):
        hashedPW = generate_password_hash(password)
        self.repo.create_user(username,hashedPW)

    def authenticate(self, username, password):
        user = self.repo.get_user_by_username(username)

        if not user or not check_password_hash(user.password, password):
            raise ValueError("Invalid credentials")

        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(days=7)

        payload = {
            "user_id": user.id,
            "exp": expires_at
        }

        token = jwt.encode(payload, Config.KEY, algorithm="HS256")

        expires_in = int((expires_at - now).total_seconds())

        response = {
            "token": token,
            "expires_at": expires_at.isoformat(),
            "expires_in": expires_in
        }

        return response
    

    
    def get_current_user(self):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(
                token,
                Config.KEY,
                algorithms=["HS256"]
            )

            user_id = payload["user_id"]

            user = self.repo.get_user_by_id(user_id)

            return user

        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
