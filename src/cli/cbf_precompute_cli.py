import click
from flask.cli import with_appcontext
from ..services.cbf_service import CbfService


@click.command("precompute")
@with_appcontext
def cbf_precompute():
    cbf = CbfService()
    print("Mulai proses TF-IDF")
    df = cbf.compute_tfidf_manual()
    print("TF-IDF selesai. Jumlah data:", len(df))

    print("Mulai hitung similarity")
    rows = cbf.compute_similarity()
    print("Similarity selesai", len(rows))

    print("Precompute selesai")