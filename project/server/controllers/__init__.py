from flask import Blueprint

from .registerAPI import RegisterAPI
from .loginAPI import LoginAPI
from .logout import LogoutAPI
from .refresh import RefreshToken
from .userAPI import UserAPI
from .protected import ProtectedAPI
from .bfxAPI import BfxAPI


auth_blueprint = Blueprint('auth', __name__)
api_blueprint = Blueprint('api', __name__)

registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
logout_view = LogoutAPI.as_view('logout_api')
refresh_view = RefreshToken.as_view('refresh_api')
user_status_view = UserAPI.as_view('user_api')
protected_view = ProtectedAPI.as_view('protected_api')

bfx_view = BfxAPI.as_view('ticker_prices')

auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/logout',
    view_func=logout_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/refresh',
    view_func=refresh_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/status',
    view_func=user_status_view,
    methods=['POST', 'GET']
)


auth_blueprint.add_url_rule(
    '/protected',
    view_func=protected_view,
    methods=['GET']
)
api_blueprint.add_url_rule(
    '/api/tickers',
    view_func=bfx_view,
    methods=['GET', 'POST']
)
