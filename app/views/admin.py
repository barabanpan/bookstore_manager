from flask.blueprints import Blueprint
from flask import render_template

from app.models.user_model import UserModel


admin_bp = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates')


@admin_bp.route("users")
def users():
    """For viewing list of users."""
    try:
        users = UserModel.return_all()
    except Exception as e:
        return {"message": "Something else went wrong while creating: " + repr(e)}, 500

    return render_template("admin/users.html", data=users)
