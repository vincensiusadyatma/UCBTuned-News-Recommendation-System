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

  
    if not data:
        return jsonify({
            "status": "error",
            "message": "Body JSON tidak boleh kosong"
        }), 400

    user_id = data.get("user_id")
    news_id = data.get("news_id")
    feedback = data.get("feedback")

    if user_id is None or news_id is None or feedback is None:
        return jsonify({
            "status": "error",
            "message": "user_id, news_id, dan feedback wajib diisi"
        }), 400

    if feedback not in [0, 1]:
        return jsonify({
            "status": "error",
            "message": "feedback harus 0 (dislike) atau 1 (like)"
        }), 400

    session = Session()

    try:
        new_feedback = NewsFeedback(
            user_id=user_id,
            news_id=news_id,
            feedback=feedback
        )

        session.add(new_feedback)
        session.commit()

        return jsonify({
            "status": "success",
            "message": "Feedback berhasil disimpan",
            "data": {
                "user_id": user_id,
                "news_id": news_id,
                "feedback": feedback
            }
        })

    except Exception as e:
        session.rollback()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:
        session.close()