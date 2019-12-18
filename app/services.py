from . import repositories
from . import errors
from . import create_access_token
from . import create_refresh_token
from . import models
from . import get_raw_jwt
from . import get_jwt_identity
from . import Message
from . import mail
from . import app
from . import validators
from . import id_token
from . import requests


class AuthService:
    def __init__(self):
        self._user_repository = repositories.UserRepository()

    @validators.validate_json
    @validators.validate_schema(validators.sign_in_schema)
    def sign_in(self, data):
        """
        Sign in method for trivial native sign in
        with provided password and unique email
        :param data: dict
        :return: dict
        """

        # Parse data
        user_email = data.get('email')
        user_password = data.get('password')

        # Receive user by provided email
        user = self._user_repository.find_by_email(user_email)

        # Forbid sign in if user do not exists in database
        if not user:
            message = 'User doesnt exist with given credentials'
            raise errors.WrongAuthCredentials(message)

        # Forbid sign in if user is not verified
        if not user.verified:
            message = 'User was not verified'
            raise errors.NotVerified(message)

        # Check if provided password is correct
        # by comparing pass hashes
        password_is_valid = self._user_repository \
            .compare_password_with_hash(user_password, user.password)

        # If password is valid then sign in user and return access data
        if password_is_valid:
            access_token = create_access_token(identity=user_email)
            refresh_token = create_refresh_token(identity=user_email)
            return {
                'message': 'Logged in as {}'.format(user.email),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            message = 'User doesnt exist with given credentials'
            raise errors.WrongAuthCredentials(message)

    @validators.validate_json
    @validators.validate_schema(validators.sign_up_schema)
    def sign_up(self, data):
        """
        Sign up user by provided email and password.
        The provided email must be unique.
        After user was created in database.
        that method send verification email to the user.
        Return the info details.
        :param data: dict
        :return: dict
        """

        # Parse data
        user_email = data.get('email')
        user_password = data.get('password')

        # Create user by passed data
        user = self._user_repository \
            .create_by_email_and_pass(user_email, user_password)

        # Send verification letter to the user
        msg = Message("Email verification", recipients=[user.email])
        msg.html = "To verify email please use the <a href={}://{}/#/verify/{}>link<a>" \
            .format(app.config['SSL'], app.config['SERVER_HOST'], user.email_token)
        mail.send(msg)

        # Return info response
        return {
            'message': 'User must be verified',
        }

    @validators.validate_json
    @validators.validate_schema(validators.verify_schema)
    def verify(self, data):
        """
        Verify user by email token send during sign up.
        Receive user by that token and verify that user.
        Set verification token to null to blacklist it.
        Return all necessary access info.
        :param data: dict
        :return: dict
        """

        # Parse data
        email_token = data.get('email_token')

        # Verify user
        user = self._user_repository.verify(email_token)

        # Return all necessary access data
        access_token = create_access_token(identity=user.email)
        refresh_token = create_refresh_token(identity=user.email)

        return {
            'message': 'User was verified',
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    @staticmethod
    def refresh_token():
        """
        Refresh the access token by
        specifying in headers refresh token.
        :return: dict
        """
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}

    @staticmethod
    def logout():
        """
        Logout user from access to all protected routes.
        Other words blacklist access jwt token.
        :return: dict
        """
        # Get raw jwt
        jti = get_raw_jwt()['jti']

        # Revoke token by raw jwt and add it to revoked tokens
        revoked_token = models.RevokedTokenModel(jti=jti)
        revoked_token.add()

        # Return success message
        return {
            'message': 'User was logged out'
        }

    @validators.validate_json
    @validators.validate_schema(validators.sign_in_social_schema)
    def sign_in_social(self, data):
        social_data = data.get('social_data')
        social_provider = data.get('social_provider')

        if social_provider == 'google':
            return self._sign_in_by_google(social_data)

    def _sign_in_by_google(self, social_data):
        social_token = social_data.get('social_token')

        if not social_token:
            message = 'Social token was not provided'
            raise errors.FieldNotValid(message)

        try:
            id_info = id_token.verify_oauth2_token(social_token, requests.Request(), app.config.get('GOOGLE_CLIENT_ID'))

            if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            social_id = id_info['sub']
            email = id_info['email']

            user = self._user_repository.create_by_email_and_social_id_or_receive(email, social_id)

            access_token = create_access_token(identity=user.email)
            refresh_token = create_refresh_token(identity=user.email)

            return {
                'message': 'User was signed in',
                'access_token': access_token,
                'refresh_token': refresh_token
            }

        except ValueError:
            message = 'Incorrect social token specified'
            raise errors.SocialAuthError(message)
