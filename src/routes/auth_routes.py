from flask import Blueprint
from flask import request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from flask import jsonify
from src.services.auth_service import AuthService

auth_bp = Blueprint("auth",__name__)
service = AuthService()

@auth_bp.route("/")
def login():
    return "Login page"

@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "No Data"
            }), 400

        elif not data.get("username") or not data.get("password"):
            return jsonify({
                "status": "error",
                "message": "Username and password are required"
            }), 400

        else:
            username = data.get("username")
            password = data.get("password")

            service.register(username, password)

            return jsonify({
                "status": "success",
                "message": "User registered successfully"
            }), 201

    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500