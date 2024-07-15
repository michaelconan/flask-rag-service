import pytest
import os
from flask.testing import FlaskCliRunner
from flask_rag_service import db


def test_setup_db(cli: FlaskCliRunner):
    # GIVEN
    # Drop all tables to reset
    db.drop_all()

    # WHEN
    # Run command to create tables
    result = cli.invoke(args=["setup-db"])

    # THEN
    tables = db.metadata.tables
    assert len(tables) > 2
