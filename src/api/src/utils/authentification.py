
## Authentification util functions
##
## All the functions that are used to perform authentification
##
## functions:
## - authentification_required: function used as a decorator for every flask route that needs
##                              to check if the token in the body of the request corresponds
##                              to the admin token 

import jwt
from functools import wraps

def authentification_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.json['token']
        if not token:
            return jsonify({'error': 'token is missing'}), 403
        try:
            jwt.decode(token, app.config['secret_key'], algorithms="HS256")
        except Exception as error:
            return jsonify({'error': 'token is invalid/expired'})
        return f(*args, **kwargs)
    return decorated

