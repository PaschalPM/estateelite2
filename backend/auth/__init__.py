from flask import Blueprint
from .views.api import register

''' API '''
auth_api_bp = Blueprint('auth_api', __name__, url_prefix='/api/auth')
auth_api_bp.add_url_rule('/register', view_func=register, methods=['POST'])