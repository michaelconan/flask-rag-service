import pytest
from typing import Generator
from flask import Flask
from flask.testing import FlaskClient
from flask.testing import FlaskCliRunner
from flask_rag_service import create_app


@pytest.fixture()
def app() -> Generator[Flask, None, None]:
    """Fixture to create flask app from factory
    and initiate app context
    """
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        },
    )

    with app.app_context():
        yield app


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    """Fixture to create test client for view tests"""
    return app.test_client()


@pytest.fixture()
def cli(app: Flask) -> FlaskCliRunner:
    """Fixture to create test CLI runner for command tests"""
    return app.test_cli_runner()
