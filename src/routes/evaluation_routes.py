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

        K_VALUES = [1, 2, 3, 4, 5]

        user_k_metrics = {}

        for log in logs:
            user_id = log.user_id

            recs = [int(x) for x in (log.recommendations or [])]
            rels = [int(x) for x in (log.relevants or [])]

            if not recs:
                continue

            if user_id not in user_k_metrics:
                user_k_metrics[user_id] = {
                    k: {"p": [], "r": [], "ap": []}
                    for k in K_VALUES
                }

            for k in K_VALUES:
                p = service.precision_at_k(recs, rels, k)
                r = service.recall_at_k(recs, rels, k)
                ap = service.average_precision(recs, rels, k)

                user_k_metrics[user_id][k]["p"].append(p)
                user_k_metrics[user_id][k]["r"].append(r)
                user_k_metrics[user_id][k]["ap"].append(ap)

        evaluation_results = []

        for user_id, k_data in user_k_metrics.items():
            for k, metrics in k_data.items():

                if not metrics["p"]:
                    continue

                n = len(metrics["p"])

                avg_p = sum(metrics["p"]) / n
                avg_r = sum(metrics["r"]) / n
                avg_ap = sum(metrics["ap"]) / n

                f1 = service.f1_score(avg_p, avg_r)

                evaluation_results.append({
                    "user_id": user_id,
                    "precision": avg_p,
                    "recall": avg_r,
                    "f1_score": f1,
                    "average_precision": avg_ap,
                    "k": k
                })

        service.repo.delete_all()
        service.repo.save_bulk(evaluation_results)

        summary_by_k = []

        for k in K_VALUES:
            k_rows = [
                r for r in evaluation_results
                if r["k"] == k
            ]

            if not k_rows:
                continue

            n = len(k_rows)

            summary_by_k.append({
                "k": k,
                "precision": sum(r["precision"] for r in k_rows) / n,
                "recall": sum(r["recall"] for r in k_rows) / n,
                "f1_score": sum(r["f1_score"] for r in k_rows) / n,
                "map": sum(r["average_precision"] for r in k_rows) / n
            })

        global_summary = service.calculate_mean_metrics(evaluation_results)

        return jsonify({
            "message": "Evaluation synced successfully",
            "total_rows": len(evaluation_results),
            "summary_by_k": summary_by_k,
            "global_summary": global_summary
        })

    except Exception as e:
        print("ERROR:", e)
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
            uid = r.user_id

            if uid not in user_map:
                user_map[uid] = {"user_id": uid}

            user_map[uid][f"k{r.k}"] = r.precision

        return jsonify(list(user_map.values()))

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
            uid = r.user_id

            if uid not in user_map:
                user_map[uid] = {"user_id": uid}

            user_map[uid][f"k{r.k}"] = r.recall

        return jsonify(list(user_map.values()))

    finally:
        session.close()


@evaluation_bp.route("/evaluation/f1", methods=["GET"])
def get_f1():
    session = Session()

    try:
        service = EvaluationService(session)
        results = service.repo.get_all()

        user_map = {}

        for r in results:
            uid = r.user_id

            if uid not in user_map:
                user_map[uid] = {"user_id": uid}

            user_map[uid][f"k{r.k}"] = r.f1_score

        return jsonify(list(user_map.values()))

    finally:
        session.close()


@evaluation_bp.route("/evaluation/ap", methods=["GET"])
def get_ap():
    session = Session()

    try:
        service = EvaluationService(session)
        results = service.repo.get_all()

        user_map = {}

        for r in results:
            uid = r.user_id

            if uid not in user_map:
                user_map[uid] = {"user_id": uid}

            user_map[uid][f"k{r.k}"] = r.average_precision or 0

        return jsonify(list(user_map.values()))

    finally:
        session.close()

@evaluation_bp.route("/evaluation/map", methods=["GET"])
def get_map():
    session = Session()

    try:
        service = EvaluationService(session)
        results = service.repo.get_all()


        evaluation_data = [
            {
                "user_id": r.user_id,
                "average_precision": r.average_precision or 0
            }
            for r in results
        ]

        map_score = service.calculate_map(evaluation_data)

        return jsonify({
            "map": map_score
        })

    finally:
        session.close()

@evaluation_bp.route("/evaluation/user/<int:user_id>", methods=["GET"])
def get_metric_by_user(user_id):
    session = Session()

    try:
        service = EvaluationService(session)

        data = service.get_metric_by_user_id(user_id)

        if not data:
            return jsonify({
                "message": f"User {user_id} tidak ditemukan"
            }), 404

        return jsonify(data)

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"message": "Internal server error"}), 500

    finally:
        session.close()

@evaluation_bp.route("/evaluation/general/precision", methods=["GET"])
def get_general_precision():
    session = Session()

    try:
        service = EvaluationService(session)

        data = service.get_general_metrics("precision")

        return jsonify(data)

    finally:
        session.close()

@evaluation_bp.route("/evaluation/general/recall", methods=["GET"])
def get_general_recall():
    session = Session()

    try:
        service = EvaluationService(session)

        data = service.get_general_metrics("recall")

        return jsonify(data)

    finally:
        session.close()

@evaluation_bp.route("/evaluation/general/f1", methods=["GET"])
def get_general_f1():
    session = Session()

    try:
        service = EvaluationService(session)

        data = service.get_general_metrics("f1_score")

        return jsonify(data)

    finally:
        session.close()

@evaluation_bp.route("/evaluation/general/ap", methods=["GET"])
def get_general_ap():
    session = Session()

    try:
        service = EvaluationService(session)

        data = service.get_general_metrics("average_precision")

        return jsonify(data)

    finally:
        session.close()