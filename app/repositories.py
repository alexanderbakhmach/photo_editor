from . import models
from . import errors
from . import sha256
from . import hashlib


class UserRepository:

    @staticmethod
    def find_by_email(email: str):
        user = models.UserModel.query.filter_by(email=email).first()
        return user

    @staticmethod
    def find_by_email_token(email_token: str):
        user = models.UserModel.query.filter_by(email_token=email_token).first()
        return user

    def create_by_email_and_pass(self, email: str, password: str):
        old_user = self.find_by_email(email)

        if old_user:
            raise errors.InstanceExistsException('User already exists')

        password_hash = UserRepository.create_user_password_hash(password)
        email_token = UserRepository.create_user_email_token(email)
        user = models.UserModel(
            email=email,
            password=password_hash,
            email_token=email_token
        )

        user.save_to_db()

        return user

    def create_by_email_and_social_id_or_receive(self, email: str, social_id: str):
        old_user = self.find_by_email(email)

        if old_user:
            return old_user

        social_id_hash = UserRepository.create_user_social_id_hash(social_id)
        user = models.UserModel(
            email=email,
            social_id=social_id_hash,
            verified=True
        )

        user.save_to_db()

        return user

    def verify(self, email_token: str):
        user = self.find_by_email_token(email_token)

        if not user:
            message = 'Wrong email verification token'
            raise errors.InstanceDoNotExistsException(message)

        user.email_token = None
        user.verified = True
        user.save_to_db()

        return user

    @staticmethod
    def compare_password_with_hash(password: str, password_hash: str):
        return sha256.verify(password, password_hash)

    @staticmethod
    def create_user_password_hash(password: str):
        return sha256.hash(password)

    @staticmethod
    def create_user_social_id_hash(social_id: str):
        return sha256.hash(social_id)

    @staticmethod
    def create_user_email_token(email: str):
        return hashlib.sha224(email.encode('utf-8')).hexdigest()
