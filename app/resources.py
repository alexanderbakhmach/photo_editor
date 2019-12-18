from . import Resource
from . import jwt_refresh_token_required
from . import jwt_required
from . import services
from . import parsers


class SignInResource(Resource):
    def post(self):
        data = parsers.sign_in_parser.parse_args()
        auth_service = services.AuthService()
        return auth_service.sign_in(data)


class SignInSocialResource(Resource):
    def post(self):
        data = parsers.sign_in_social_parser.parse_args()
        auth_service = services.AuthService()
        return auth_service.sign_in_social(data)


class VerifyResource(Resource):
    def post(self):
        data = parsers.verify_parser.parse_args()
        auth_service = services.AuthService()
        return auth_service.verify(data)


class SignUpResource(Resource):
    def post(self):
        data = parsers.sign_up_parser.parse_args()
        auth_service = services.AuthService()
        return auth_service.sign_up(data)


class LogOutResource(Resource):
    @jwt_required
    def post(self):
        auth_service = services.AuthService()
        return auth_service.logout()


class LogOutRefreshResource(Resource):
    @jwt_refresh_token_required
    def post(self):
        auth_service = services.AuthService()
        return auth_service.logout()


class TokenRefreshResource(Resource):
    @jwt_refresh_token_required
    def post(self):
        auth_service = services.AuthService()
        return auth_service.refresh_token()
