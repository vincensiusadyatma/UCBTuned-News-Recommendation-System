import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from src.models import News
from src.config import Session


def seed_news():
    df = pd.read_csv("dataset/news_preprocess.csv")

    session = Session()

    total_inserted = 0

    for i, row in df.iterrows():
        title = str(row["Judul"]).strip()
        content = str(row["Content"]).strip()

        fake_link = f"seeded://news/{i}"

        exists = session.query(News).filter_by(link=fake_link).first()
        if exists:
            continue

        news = News(
            title=title,
            content=content,
            time=datetime.utcnow(),
            link=fake_link,
            source="dataset"
        )

        session.add(news)
        total_inserted += 1

    session.commit()
    session.close()

