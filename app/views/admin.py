from flask.blueprints import Blueprint
from flask_jwt_extended import jwt_required

from app.models.manager_model import ManagerModel


admin_bp = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates')


@admin_bp.route("managers")
@jwt_required()
def managers():
    """For viewing list of users."""
    managers = ManagerModel.return_all_json()
    return managers
