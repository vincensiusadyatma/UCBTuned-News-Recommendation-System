import click
from flask.cli import with_appcontext
from ..seeders import seed_news

@click.command("seed")
@with_appcontext
def news_seeding():
    seed_news()