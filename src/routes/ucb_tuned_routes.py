from flask import Blueprint, jsonify, request
from src.services.ucb_tuned_service import UcbTunedService
from src.config import Session
from src.models import NewsFeedback

ucb_tuned_bp = Blueprint("recommendation", __name__, url_prefix="/ucb/")


@ucb_tuned_bp.route("/<int:news_id>", methods=["GET"])
def recommend(news_id):
    top_k = request.args.get("top_k", default=5, type=int)

    service = UcbTunedService()
    try:
        results = service.recommend(news_id=news_id, top_k=top_k)
        return jsonify({
            "status": "success",
            "news_id": news_id,
            "total": len(results),
            "data": results
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    finally:
        service.close()


@ucb_tuned_bp.route("/feedback", methods=["POST"])
def store_feedback():
    """
    POST /api/recommendations/feedback
    Body JSON:
    {
        "user_id": 1,
        "news_id": 10,
        "feedback": 1   # 1 = klik, 0 = skip
    }
    """
    payload = request.get_json()

    user_id = payload.get("user_id")
    news_id = payload.get("news_id")
    feedback = payload.get("feedback")

    if user_id is None or news_id is None or feedback is None:
        return jsonify({
            "status": "error",
            "message": "user_id, news_id, dan feedback wajib diisi"
        }), 400

    session = Session()
    try:
        fb = NewsFeedback(
            user_id=user_id,
            news_id=news_id,
            feedback=feedback
        )
        session.add(fb)
        session.commit()

        return jsonify({
            "status": "success",
            "message": "Feedback berhasil disimpan"
        })
    except Exception as e:
        session.rollback()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    finally:
        session.close()