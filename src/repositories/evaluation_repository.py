from src.config import Session
from src.models import EvaluationResult


class EvaluationRepository:
    def __init__(self):
        self.session = Session()

    # =========================
    # INSERT BULK (utama)
    # =========================
    def save_bulk(self, evaluations: list[dict]):
        objs = [
            EvaluationResult(
                user_id=ev["user_id"],
                precision=ev["precision"],
                recall=ev["recall"],
                f1_score=ev["f1_score"],
                mean_average_precision=ev["map_score"],
                k=ev["k"]
            )
            for ev in evaluations
        ]

        self.session.add_all(objs)
        self.session.commit()

        return objs

    # =========================
    # GET
    # =========================
    def get_all(self):
        return self.session.query(EvaluationResult).all()

    def get_by_user(self, user_id: int):
        return (
            self.session.query(EvaluationResult)
            .filter(EvaluationResult.user_id == user_id)
            .all()
        )

    # =========================
    # DELETE
    # =========================
    def delete_all(self):
        self.session.query(EvaluationResult).delete()
        self.session.commit()

    def close(self):
        self.session.close()