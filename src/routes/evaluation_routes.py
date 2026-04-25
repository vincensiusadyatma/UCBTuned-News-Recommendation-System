from flask import Blueprint, jsonify
from src.config import Session
from src.services.evaluation_service import EvaluationService
from src.repositories.recommendation_log_repository import RecommendationLogRepository

evaluation_bp = Blueprint("evaluation", __name__)


@evaluation_bp.route("/evaluation/sync", methods=["POST"])
def sync_evaluation():
    session = Session()

    try:
        log_repo = RecommendationLogRepository()
        logs = log_repo.get_all()

        if not logs:
            return jsonify({"message": "No logs found"}), 400

        service = EvaluationService(session)

        K_VALUES = [1, 3, 5]

        user_k_metrics = {}

        for log in logs:
            user_id = log.user_id
            recs = log.recommendations or []
            rels = log.relevants or []

            if user_id not in user_k_metrics:
                user_k_metrics[user_id] = {
                    k: {"p": [], "r": []} for k in K_VALUES
                }

            for k in K_VALUES:
                if len(recs) < k:
                    continue

                p = service.precision_at_k(recs, rels, k)
                r = service.recall_at_k(recs, rels, k)

                user_k_metrics[user_id][k]["p"].append(p)
                user_k_metrics[user_id][k]["r"].append(r)


        evaluation_results = []

        for user_id, k_data in user_k_metrics.items():
            for k, metrics in k_data.items():

                if not metrics["p"]:
                    continue

                n = len(metrics["p"])

                avg_p = sum(metrics["p"]) / n
                avg_r = sum(metrics["r"]) / n

                evaluation_results.append({
                    "user_id": user_id,
                    "precision": avg_p,
                    "recall": avg_r,
                    "f1_score": None,
                    "map_score": None,
                    "k": k
                })

  
        service.repo.delete_all()
        service.repo.save_bulk(evaluation_results)


        summary = service.calculate_mean_metrics(evaluation_results)

        return jsonify({
            "message": "Evaluation synced successfully",
            "summary": summary,
            "total_rows": len(evaluation_results) 
        })

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500

    finally:
        session.close()
        
@evaluation_bp.route("/evaluation/precision", methods=["GET"])
def get_precision():
    session = Session()

    try:
        service = EvaluationService(session)
        results = service.repo.get_all()

        user_map = {}

        for r in results:
            user_id = r.user_id

            if user_id not in user_map:
                user_map[user_id] = {
                    "user_id": user_id,
                    "k1": 0,
                    "k3": 0,
                    "k5": 0
                }

            if r.k == 1:
                user_map[user_id]["k1"] = r.precision
            elif r.k == 3:
                user_map[user_id]["k3"] = r.precision
            elif r.k == 5:
                user_map[user_id]["k5"] = r.precision

        return jsonify(list(user_map.values()))

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500

    finally:
        session.close()

@evaluation_bp.route("/evaluation/recall", methods=["GET"])
def get_recall():
        session = Session()

        try:
            service = EvaluationService(session)
            results = service.repo.get_all()

            user_map = {}

            for r in results:
                user_id = r.user_id

                if user_id not in user_map:
                    user_map[user_id] = {
                        "user_id": user_id,
                        "k1": 0,
                        "k3": 0,
                        "k5": 0
                    }

                if r.k == 1:
                    user_map[user_id]["k1"] = r.recall
                elif r.k == 3:
                    user_map[user_id]["k3"] = r.recall
                elif r.k == 5:
                    user_map[user_id]["k5"] = r.recall

            return jsonify(list(user_map.values()))

        except Exception as e:
            print(e)
            return jsonify({"message": "Internal server error"}), 500

        finally:
            session.close()