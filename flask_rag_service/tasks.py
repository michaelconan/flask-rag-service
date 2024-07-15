import time
import logging
from celery import shared_task
from flask import current_app


@shared_task()
def preprocess_document(file: str) -> None:
    time.sleep(5)
    logging.info(f"Testing app: {current_app.config['TESTING']}")
