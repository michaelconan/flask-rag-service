from flask import Blueprint
from flask import request
from flask import jsonify
from flask import current_app
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from .models import db, User, Collection
from . import tasks

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.get("/users/<id>/collections")
@jwt_required
def user_collections(id: str) -> dict[str, object]:
    """Method to list collections for a user.
    ---
    parameters:
      - name: palette
        in: path
        type: int
        required: true
    responses:
      200:
        description: A list of collections
        examples:
          collections: [{'id': 1, 'name':'test'}]
    """
    # Get collections for authenticated user
    current_user = get_jwt_identity()
    collections = (
        db.session.query(Collection)
        .join(
            Collection.user,
        )
        .filter_by(User.username == current_user)
        .scalars()
    )
    # Return collections
    return jsonify(
        collections=collections,
    )
