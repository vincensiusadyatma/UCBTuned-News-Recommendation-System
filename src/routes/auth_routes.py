from flask import Blueprint
from flask import request
from flask import jsonify
from src.services.auth_service import AuthService

auth_bp = Blueprint("auth",__name__)
service = AuthService()

@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"message": "No data"}), 400

        if not data.get("username"):
            return jsonify({"message": "Username is required"}), 400

        if not data.get("password"):
            return jsonify({"message": "Password is required"}), 400

        username = data.get("username")
        password = data.get("password")

        result = service.authenticate(username, password)

        return jsonify({
            "message": "Login success",
            "token": result["token"],
            "expires_at": result["expires_at"],
            "expires_in": result["expires_in"]
        }), 200

    except ValueError as e:
        return jsonify({"message": str(e)}), 401

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500



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

    except ValueError as e :
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

    except Exception as e:
        print(e)
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500
    
@auth_bp.route("/profile")
def profile():
    user = service.get_current_user()

    if not user:
        return jsonify({"message": "Unauthorized"}), 401

    return jsonify({
        "message": "Success",
        "user_id" : user.id,
        "username" : user.username
    })
