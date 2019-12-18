from . import wraps
from . import request
from . import jsonify
from . import jsonschema

sign_in_schema = {
    'type': 'object',
    'properties': {
        'password': {
            'type': 'string',
            'minLength': 6,
            'maxLength': 30
        },
        'email': {
            'type': 'string',
            'pattern': '^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$',
            'maxLength': 60
        },
    },
}

sign_in_social_schema = {
    'type': 'object',
    'properties': {
        'social_data': {
            'type': 'object',
        },
        'social_provider': {
            'type': 'string',
            'enum': ['google']
        },
    },
}

sign_up_schema = {
    'type': 'object',
    'properties': {
        'password': {
            'type': 'string',
            'minLength': 6,
            'maxLength': 30
        },
        'email': {
            'type': 'string',
            'pattern': '^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$',
            'maxLength': 60
        },
    },
}

verify_schema = {
    'type': 'object',
    'properties': {
        'email_token': {
            'type': 'string',
            'maxLength': 150
        }
    },
}


def validate_json(f):
    """
    Validate that input arg is in valid json format
    :param f:
    :return:
    """

    @wraps(f)
    def wrapper(*args, **kw):
        try:
            json = request.json
        except Exception as e:
            msg = "payload must be a valid json"
            return jsonify({"error": msg}), 422
        return f(*args, **kw)

    return wrapper


def validate_schema(schema):
    """
    Validate that input request is valid by schema rules passed
    :param schema:
    :return:
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            print(request.json)
            jsonschema.validate(request.json, schema)

            return f(*args, **kw)

        return wrapper

    return decorator
