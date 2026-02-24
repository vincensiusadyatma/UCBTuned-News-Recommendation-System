import click
from flask.cli import with_appcontext
from ..services.cbf_service import ContentBasedPrecomputeService

@click.command("precompute")
@with_appcontext
def cbf_precompute():
    cbf = ContentBasedPrecomputeService()
    cbf.compute_tfidf()
    cbf.compute_similarity()