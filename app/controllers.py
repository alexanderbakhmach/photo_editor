from . import app
from . import jsonify
from . import api
from . import resources
from . import jwt_required

api.add_resource(resources.SignInResource, '/sign-in')
api.add_resource(resources.SignInSocialResource, '/sign-in/social')
api.add_resource(resources.SignUpResource, '/sign-up')
api.add_resource(resources.LogOutResource, '/logout')
api.add_resource(resources.LogOutRefreshResource, '/logout-refresh')
api.add_resource(resources.TokenRefreshResource, '/token/refresh')
api.add_resource(resources.VerifyResource, '/verify')


@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'info': {
            'Version': '1.0.0a',
            'Description': 'The photo editor api'
        }
    })
