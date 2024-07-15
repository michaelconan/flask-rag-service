"""
test_tasks.py

This module demonstrates how to use pytest to unit test Celery tasks with the Flask + Celery application factory pattern.
"""

import pytest
from flask import Flask
from flask_rag_service import tasks


def test_add_task(app: Flask):
    """Unit test to validate the celery add task"""
    # GIVEN
    number1 = 1
    number2 = 2

    # WHEN
    result = tasks.add(number1, number2)

    # THEN
    assert result == 3
