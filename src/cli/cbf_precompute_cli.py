import click
from flask.cli import with_appcontext
from ..services.cbf_service import CbfService

@click.command("precompute")
@with_appcontext
def cbf_precompute():
    cbf = CbfService()
    cbf.compute_tfidf()
    cbf.compute_similarity()