from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from authertest.auther_utils.utils_account import back_jwt


class LoginMiddleware(MiddlewareMixin):
    def process_request(self, request, *args, **kwargs):
        if request.path_info == '/account/login/':
            return None
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            data = {
                'tip': -100,
                'msg': '用户未登录',
                'data': {}
            }
            return JsonResponse(data)
        return None

