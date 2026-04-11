from flask import Blueprint, jsonify, request
from src.services.cbf_service import CbfService

cbf_bp = Blueprint("cbf", __name__)

service = CbfService()

@cbf_bp.route("/cbf/<int:news_id>")
def recommend_news(news_id):
    candidate_size = request.args.get("candidate_size", default=20, type=int)

    results = service.recomendation(
        news_id,
        candidate_size=candidate_size
    )

    return jsonify({
        "news_id": news_id,
        "candidate_size": candidate_size,
        "total": len(results),
        "data": results
    })