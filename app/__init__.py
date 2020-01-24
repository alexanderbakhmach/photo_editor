import jsonschema
import hashlib
import requests

# Import flask and template operators
from flask import Flask
from flask import jsonify
from flask import request

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Import flask resfull
from flask_restful import Resource
from flask_restful import Api
from flask_restful import reqparse

# Import sha for making password hashes
from passlib.hash import pbkdf2_sha256 as sha256

# Import and  jwt manager to enable jwt support
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import jwt_refresh_token_required
from flask_jwt_extended import get_jwt_identity
from flask_cors import CORS
from flask_cors import cross_origin
from flask_jwt_extended import get_raw_jwt

from functools import wraps

from flask_mail import Mail
from flask_mail import Message

from google.oauth2 import id_token
from google.auth.transport import requests

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Create api instance
api = Api(app)

# Create JWT manager instance
jwt = JWTManager(app)

mail = Mail(app)

# Add CORS support
cors = CORS(app)


from . import models
from . import errors


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)


@app.before_first_request
def create_tables():
    db.create_all()


from . import controllers
