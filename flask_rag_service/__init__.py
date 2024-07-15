from celery import Celery
from celery import Task
from flask import Flask
from flask import session
from flask import redirect
from flask import url_for
from flask import render_template
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_bcrypt import Bcrypt
from flasgger import Swagger
from .models import db


def create_app() -> Flask:
    # Define and configure Flask app
    app = Flask(__name__)
    app.config.from_pyfile("config.py", silent=True)

    # Initialize Celery, SQLAlchemy, JWT, Swagger extensions
    celery_init_app(app)
    db.init_app(app)
    jwt = JWTManager(app)
    app.extensions["jwt"] = jwt
    bcrypt = Bcrypt(app)
    app.extensions["bcrypt"] = bcrypt
    # Custom configuration to limit Swagger to auth / api routes
    swagger = Swagger(app, config=app.config['SWAGGER_CONFIG'])
    app.extensions["swagger"] = swagger

    # Define base index route
    @app.get("/")
    @jwt_required(optional=True)
    def index() -> str:
        """Index page, redirect to login if no token available

        Returns:
            str: Index or login page
        """
        # Check if user is logged in
        current_user = get_jwt_identity()
        if current_user:
            return render_template("index.html")
        else:
            return redirect(url_for("login"))

    @app.get("/login")
    def login() -> str:
        """Login page to sign up or provide credentials

        Returns:
            str: Login page with signup/in form
        """
        return render_template("login.html")

    # Register blueprints for auth and API
    from . import auth
    from . import views

    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(views.api_bp)

    return app


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app
