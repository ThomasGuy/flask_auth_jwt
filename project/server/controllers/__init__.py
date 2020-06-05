from flask import Blueprint

from .registerAPI import RegisterAPI

auth_blueprint = Blueprint('auth', __name__)

registration_view = RegisterAPI.as_view('register_api')

auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)
