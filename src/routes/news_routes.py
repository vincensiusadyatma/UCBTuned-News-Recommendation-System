from flask import Blueprint, jsonify, request
from src.services.news_service import NewsService

news_bp = Blueprint("news_bp", __name__, url_prefix="/news")
news_service = NewsService()

@news_bp.route("", methods=["GET"])
def get_news():
    news_list = news_service.get_all_news()
    return jsonify([{
        "id": n.id,
        "title": n.title,
        "content" : n.content
    } for n in news_list])


@news_bp.route("/page", methods=["GET"])
def get_news_per_page():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 20))
    news_list = news_service.get_all_news_by_page(page, per_page)
    total_pages = news_service.get_total_pages(per_page)
    return jsonify({
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages,
        "news": [{
            "id": n.id,
            "title": n.title,
            "content" : n.content
        } for n in news_list]
    })

@news_bp.route("/total-pages", methods=["GET"])
def get_total_pages():

    per_page = int(request.args.get("per_page", 20))

    total_pages = news_service.get_total_pages(per_page)

    return jsonify({
        "per_page": per_page,
        "total_pages": total_pages
    })


@news_bp.route("/<int:news_id>", methods=["DELETE"])
def delete_news(news_id):
    try:
        news_service.delete_news(news_id)
        return jsonify({"message": "News deleted successfully"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@news_bp.route("/<int:news_id>", methods=["GET"])
def get_news_by_id(news_id):
    try:
        news = news_service.get_news_by_id(news_id)

        return jsonify({
            "id": news.id,
            "title": news.title,
            "content": news.content,
            "time": news.time,
            
        })

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    
@news_bp.route("/search", methods=["GET"])
def search_news():

        keyword = request.args.get("q", "")
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))

        news_list = news_service.search_news(keyword, page, per_page)

        total_pages = news_service.get_search_total_pages(keyword, per_page)

        return jsonify({
            "query": keyword,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages,
            "news": [{
                "id": n.id,
                "title": n.title,
                "content": n.content
            } for n in news_list]
        })

@news_bp.route("", methods=["POST"])
def create_news():
    try:
        data = request.get_json()

        title = data.get("title")
        content = data.get("content")

        news = news_service.create_news(title, content)

        return jsonify({
            "message": "News created successfully",
            "data": {
                "id": news.id,
                "title": news.title,
                "content": news.content
            }
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
@news_bp.route("/<int:news_id>", methods=["PUT"])
def update_news(news_id):
    try:
        data = request.get_json()

        title = data.get("title")
        content = data.get("content")

        updated_news = news_service.update_news(news_id, title, content)

        return jsonify({
            "message": "News updated successfully",
            "data": {
                "id": updated_news.id,
                "title": updated_news.title,
                "content": updated_news.content
            }
        })

    except ValueError as e:
        return jsonify({"error": str(e)}), 404