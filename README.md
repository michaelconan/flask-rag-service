# flask-rag-service

Web application and REST API Retrieval Augmented Generation microservice with distributed task preprocessing and vector database.

## Content

## Flask Application Design and Extensions

- [Flask + Celery example](https://github.com/pallets/flask/tree/main/examples/celery): Use Celery for distributed background tasks
- [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/quickstart): Object Relational Mapper (ORM) pattern to define database patterns and relationships
- [Flask BCrypt](https://flask-bcrypt.readthedocs.io/en/1.0.1/): Hash password for database storage, compare hash for login function
- [Flask JWT Extended](https://flask-jwt-extended.readthedocs.io/en/stable/index.html)
    - [Implicit Cookie Refresh](https://flask-jwt-extended.readthedocs.io/en/stable/refreshing_tokens.html#implicit-refreshing-with-cookies): Use cookies to store JWT token for web application authorization
    - [Explicity Token Refresh](https://flask-jwt-extended.readthedocs.io/en/stable/refreshing_tokens.html#token-freshness-pattern): Use refresh token pattern for API authorization
- [Flask Unit Testing (pytest)](https://flask.palletsprojects.com/en/1.1.x/testing/): Unit tests for flask views, commands and extensions


## Build and Test

Run pre-commit hooks for formatting:
`poetry run pre-commit --all-files --verbose --show-diff-on-failure`
