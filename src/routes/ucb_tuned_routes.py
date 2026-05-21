from flask import Blueprint, jsonify, request
from src.services.ucb_tuned_service import UcbTunedService
from src.config import Session
from src.models import NewsFeedback

ucb_tuned_bp = Blueprint("recommendation", __name__, url_prefix="/ucb")


@ucb_tuned_bp.route("/<int:news_id>", methods=["GET"])
def recommend(news_id):
    top_k = request.args.get("top_k", default=5, type=int)
    candidate_size = request.args.get("candidate_size", default=10, type=int)

    service = UcbTunedService()
    try:
        results = service.recommend(
            news_id=news_id,
            top_k=top_k,
            candidate_size=candidate_size
        )

        return jsonify({
            "status": "success",
            "news_id": news_id,
            "total_recommendations": len(results["recommendations"]),
            "total_candidates": len(results["all_ranked"]),
            "recommendations": results["recommendations"],
            "all_ranked": results["all_ranked"]
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:
        service.close()

@ucb_tuned_bp.route("/feedback", methods=["POST"])
def submit_feedback():
    data = request.get_json()

    service = UcbTunedService()

    try:
        result = service.submit_feedback(data)

        return jsonify({
            "status": "success",
            "message": "Feedback berhasil disimpan",
            "data": result
        })

    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:
        service.close()