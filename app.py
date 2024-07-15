from flask_rag_service import create_app
from flask_rag_service import db

app = create_app()
celery_app = app.extensions["celery"]


@app.cli.command("setup-db")
def setup_db():
    db.create_all()
