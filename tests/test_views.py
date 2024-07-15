"""
test_views.py

This module demonstrates how to use pytest to unit test Flask views with the Flask application factory pattern.
"""

import pytest
from flask.testing import FlaskClient
from flask_rag_service import tasks


def test_request_example(client: FlaskClient):
    """Unit test to validate index page view"""
    # GIVEN
    route = "/"

    # WHEN
    response = client.get(route)

    # THEN
    assert b"<h2>Celery Example</h2>" in response.data
