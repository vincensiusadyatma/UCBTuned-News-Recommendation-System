from src.config import Session
from src.models import RecommendationLog
from sqlalchemy.exc import SQLAlchemyError


class RecommendationLogRepository:
    def __init__(self):
        self.session = Session()

    def save(
        self,
        user_id: int,
        recommendations: list[int],
        relevants: list[int] | None = None
    ):
        try:
            log = RecommendationLog(
                user_id=user_id,
                recommendations=recommendations,
                relevants=relevants or []
            )

            self.session.add(log)
            self.session.commit()
            self.session.refresh(log)

            return log

        except SQLAlchemyError:
            self.session.rollback()
            raise


    def save_bulk(self, logs: list[dict]):
        try:
            objs = [
                RecommendationLog(
                    user_id=log["user_id"],
                    recommendations=log["recommendations"],
                    relevants=log.get("relevants", [])
                )
                for log in logs
            ]

            self.session.add_all(objs)
            self.session.commit()

            return objs

        except SQLAlchemyError:
            self.session.rollback()
            raise

  
    def update_relevants(self, log_id: int, relevants: list[int]):
        try:
            log = self.get_by_id(log_id)
            if not log:
                return None

            log.relevants = relevants
            self.session.commit()
            self.session.refresh(log)

            return log

        except SQLAlchemyError:
            self.session.rollback()
            raise

  
    def get_by_id(self, log_id: int):
        return (
            self.session.query(RecommendationLog)
            .filter(RecommendationLog.id == log_id)
            .first()
        )


    def get_all(self):
        return self.session.query(RecommendationLog).all()

 
    def get_by_user(self, user_id: int):
        return (
            self.session.query(RecommendationLog)
            .filter(RecommendationLog.user_id == user_id)
            .all()
        )


    def get_latest_by_user(self, user_id: int):
        return (
            self.session.query(RecommendationLog)
            .filter(RecommendationLog.user_id == user_id)
            .order_by(RecommendationLog.created_at.desc())
            .first()
        )

 
    def delete(self, log_id: int):
        try:
            log = self.get_by_id(log_id)
            if not log:
                return False

            self.session.delete(log)
            self.session.commit()
            return True

        except SQLAlchemyError:
            self.session.rollback()
            raise


    def delete_all(self):
        try:
            self.session.query(RecommendationLog).delete()
            self.session.commit()

        except SQLAlchemyError:
            self.session.rollback()
            raise


    def close(self):
        self.session.close()