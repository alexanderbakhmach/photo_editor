from . import app
from . import jsonschema
from . import jsonify


class InstanceExistsException(Exception):
    def __init__(self, message):
        super(InstanceExistsException, self).__init__(message)


class InstanceDoNotExistsException(Exception):
    def __init__(self, message):
        super(InstanceDoNotExistsException, self).__init__(message)


class WrongAuthCredentials(Exception):
    def __init__(self, message):
        super(WrongAuthCredentials, self).__init__(message)


class NotVerified(Exception):
    def __init__(self, message):
        super(NotVerified, self).__init__(message)


class FieldNotValid(Exception):
    def __init__(self, message):
        super(FieldNotValid, self).__init__(message)


class SocialAuthError(Exception):
    def __init__(self, message):
        super(SocialAuthError, self).__init__(message)


@app.errorhandler(jsonschema.ValidationError)
def handle_bad_request(e):
    return jsonify({'error': e.message}), 422


@app.errorhandler(FieldNotValid)
def handle_bad_request(e):
    return jsonify({'error': str(e)}), 422


@app.errorhandler(WrongAuthCredentials)
def handle_bad_request(e):
    return jsonify({'error': str(e)}), 403


@app.errorhandler(NotVerified)
def handle_bad_request(e):
    return jsonify({'error': str(e)}), 403


@app.errorhandler(InstanceExistsException)
def handle_bad_request(e):
    return jsonify({'error': str(e)}), 422


@app.errorhandler(SocialAuthError)
def handle_bad_request(e):
    return jsonify({'error': str(e)}), 422


@app.errorhandler(InstanceDoNotExistsException)
def handle_bad_request(e):
    return jsonify({'error': str(e)}), 404


@app.errorhandler(404)
def handle_bad_request(e):
    return jsonify({'error': 'Requested resource was not found'}), 404
