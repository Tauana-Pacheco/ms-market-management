import jwt
import datetime
from flask import request, jsonify
from functools import wraps

SECRET_KEY = 'msmarket'

def gerar_token(email):
    payload = {
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def verificar_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['email']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_obrigatorio(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace("Bearer ", "")

        if not token:
            return jsonify({'error': 'Token ausente!'}), 401

        email = verificar_token(token)
        if not email:
            return jsonify({'error': 'Token inválido ou expirado!'}), 401

        return f(email, *args, **kwargs)

    return decorada