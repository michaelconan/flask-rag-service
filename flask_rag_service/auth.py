from datetime import datetime
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import current_app
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies

from .models import db, User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.post("/users/create")
def create_user():
    """Endpoint to create a new user
    ---
    definitions:
      User:
        type: object
        properties:
          username:
            type: string
          password:
            type: string
    content:
      'application/x-www-form-urlencoded':
        schema:
          $ref: User
    responses:
      201:
        description: User successfully created
        examples:
          id: 1
          username: myuser
    """
    # App extension for password encryption
    bcrypt = current_app.extensions["bcrypt"]
    hashed_pw = bcrypt.generate_password_hash(request.form["password"])
    user = User(
        username=request.form["username"],
        password=hashed_pw,
    )
    db.session.add(user)
    db.session.commit()

    return jsonify(
        id=user.id,
        username=user.username,
    ), 201


@auth_bp.post("/login")
def auth_login():
    """Endpoint to exchange user credentials for an access token
    ---
    definitions:
      User:
        type: object
        properties:
          username:
            type: string
          password:
            type: string
    content:
      'application/x-www-form-urlencoded':
        schema:
          $ref: User
    responses:
      200:
        description: Token successfully generated
        examples:
          access_token: "eyJ0eXAiOiJKV1QiLCJhbGci..."
          refresh_token: "KV1QiLCJhbGcieyJ0eXAiOiJ..."
          expires: "2024-07-14T12:00:00Z"
      401:
        description: Invalid username or password
      404:
        description: User not found
    """
    # App extension for password encryption
    bcrypt = current_app.extensions["bcrypt"]
    # Get user from database by username
    username = request.form["username"]
    user = db.one_or_404(
        db.select(User).filter_by(username=username),
        description=f"No user named '{username}'.",
    )
    # Check password against database
    password = request.form["password"]
    if bcrypt.check_password_hash(user.password, password):
        response = jsonify(message="Login successful")
        # Generate access token and refresh token
        jwt_expires = current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
        access_token = create_access_token(identity=username, fresh=True)
        refresh_token = create_refresh_token(identity=username)
        expiration = datetime.now() + jwt_expires
        set_access_cookies(response, access_token)
        return jsonify(
            access_token=access_token, refresh_token=refresh_token, expires=expiration,
        )
    else:
        return jsonify(message="Invalid username or password"), 401


@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def auth_refresh():
    # Generate access token using refresh token
    identity = get_jwt_identity()
    jwt_expires = current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
    access_token = create_access_token(identity=identity, fresh=False)
    expiration = datetime.now() + jwt_expires
    return jsonify(access_token=access_token, expires=expiration)


@auth_bp.post("/logout")
def logout():
    response = jsonify(message="logout successful")
    unset_jwt_cookies(response)
    return response
