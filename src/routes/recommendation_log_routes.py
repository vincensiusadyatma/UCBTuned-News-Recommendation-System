from flask import Blueprint, request, jsonify
from src.services.recommendation_log_service import RecommendationLogService

recommendation_log_bp = Blueprint("recommendation_log", __name__)
service = RecommendationLogService()


@recommendation_log_bp.route("/log", methods=["POST"])
def create_log():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"status": "error", "message": "No data"}), 400

        if not data.get("user_id"):
            return jsonify({"status": "error", "message": "user_id required"}), 400

        if not data.get("recommendations"):
            return jsonify({"status": "error", "message": "recommendations required"}), 400

     
        relevants = data.get("relevants", [])

        log = service.create_log(
            user_id=data["user_id"],
            recommendations=data["recommendations"],
            relevants=relevants
        )

        return jsonify({
            "status": "success",
            "message": "recommendation log created",
            "data": {
                "id": log.id,
                "user_id": log.user_id,
                "recommendations": log.recommendations,
                "relevants": log.relevants
            }
        }), 201

    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": "Internal server error"}), 500