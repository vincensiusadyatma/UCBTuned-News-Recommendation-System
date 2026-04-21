import click
from flask.cli import with_appcontext
from ..seeders import seed_news, generate_preprocessed_csv

@click.command("seed")
@with_appcontext
def news_seeding():
    generate_preprocessed_csv()
    seed_news()