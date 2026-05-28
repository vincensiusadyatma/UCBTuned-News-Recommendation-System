import click
from flask.cli import with_appcontext
from sqlalchemy import text
from src.config import Session

@click.command("reset-db")
@with_appcontext
def reset_database():
    session = Session()

    try:
        session.execute(text("SET FOREIGN_KEY_CHECKS = 0"))

        session.execute(text("TRUNCATE TABLE evaluation_results"))
        session.execute(text("TRUNCATE TABLE news_feedbacks"))
        session.execute(text("TRUNCATE TABLE news_similarity"))
        session.execute(text("TRUNCATE TABLE recommendation_logs"))
        session.execute(text("TRUNCATE TABLE news"))
        session.execute(text("TRUNCATE TABLE users"))

        session.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

        session.commit()

        print("Database reset successfully")

    except Exception as e:
        session.rollback()
        print(f"Error: {e}")

    finally:
        session.close()