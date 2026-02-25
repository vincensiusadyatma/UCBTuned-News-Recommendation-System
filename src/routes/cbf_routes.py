from flask import Blueprint, jsonify
from src.services.cbf_service import CbfService

cbf_bp = Blueprint("cbf", __name__)

service = CbfService()

@cbf_bp .route("/cbf/<int:news_id>")
def recommend_news(news_id):
    results = service.recomendation(news_id, top_k=5)

    return jsonify({
        "news_id": news_id,
        "total": len(results),
        "data": results
    })