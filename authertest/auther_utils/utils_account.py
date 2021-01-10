import jwt
import base64

from authertest import settings


def get_jwt(id):
    encode_jwt = jwt.encode({'id': id}, settings.SECRET_KEY, algorithm='HS256')
    token = encode_jwt.decode('utf-8')
    return token


def back_jwt(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    id = data.get('id')
    return id
