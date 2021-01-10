import datetime
import json
import uuid

from django.http import JsonResponse
from authertest.account.models import AccountUser, Menus
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
# Create your views here.
from authertest.auther_utils.utils_account import get_jwt, back_jwt

"""
用户
"""


def user_login(request):
    if request.method == 'GET':
        data = {
            'tip': -1,
            'msg': '请求错误'
        }
        return JsonResponse(data)
    if request.method == 'POST':
        body_json = request.body
        body = json.loads(body_json)
        username = body.get('username')
        password = body.get('password')
        if not username or not password:
            data = {
                'tip': -1,
                'msg': '请输入用户名或者密码',
                'data': {}
            }
            return JsonResponse(data)
        user = AccountUser.objects.filter(username=username)
        if not user:
            data = {
                'tip': -1,
                'msg': '用户不存在',
                'data': {}
            }
            return JsonResponse(data)
        ret = check_password(password, user.first().password)
        if not ret:
            data = {
                'tip': -1,
                'msg': '用户名或者密码错误',
                'data': {}
            }
            return JsonResponse(data)
        token = get_jwt(user.first().id)
        account_data = {
            'id': user.first().id,
            'username': user.first().username,
            'mobile': user.first().mobile,
            'email': user.first().email,
            'token': token
        }
        data = {
            'tip': 0,
            'msg': '登录成功',
            'data': account_data
        }
        return JsonResponse(data)


def user_logout(request):
    if request.method == 'GET':
        data = {
            'tip': -1,
            'msg': '请求错误',
            'data': {}
        }
        return JsonResponse(data)
    if request.method == 'POST':
        data = {
            'tip': 0,
            'msg': '退出成功',
            'data': {}
        }
        return JsonResponse(data)


def get_menus(request):
    if request.method == 'GET':
        id = back_jwt(request)
        menus = Menus.objects.filter(menu=id)
        menu_list = []
        for menu_ in menus:
            two_menus = Menus.objects.filter(fatherid=menu_.id)
            children = []
            if two_menus:
                for two_menu in two_menus:
                    children.append({
                        'id': two_menu.id,
                        'autherName': two_menu.authname,
                        'path': two_menu.path,
                        'children': []
                    })
            menu_list.append({
                'id': menu_.id,
                'autherName': menu_.authname,
                'path': menu_.path,
                'children': children
            })
        return JsonResponse({'tip': 0, 'msg': '获取菜单列表成功', 'data': menu_list})


def get_users(request):
    if request.method == 'GET':
        id = request.GET.get('id', '')
        if id:
            users = AccountUser.objects.filter(id=id)
            if not users:
                data = {
                    'tip': -1,
                    'msg': '用户信息获取失败',
                    'data': {}
                }
                return JsonResponse(data)
            user = users.first()
            data = {
                'tip': 0,
                'msg': '用户信息获取成功',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'mobile': user.mobile,
                    'email': user.email,
                }
            }
            return JsonResponse(data)
        query = request.GET.get('query', '')
        pagenum = request.GET.get('pagenum', 1)
        pagesize = request.GET.get('pagesize', 5)
        users = AccountUser.objects.filter().all().order_by('id')
        if query:
            users = users.filter(username__icontains=query).order_by('id')
        paginator = Paginator(users, pagesize)
        page_obj = paginator.get_page(pagenum)
        user_list = []
        totalpage = users.count()
        if not users:
            data = {
                'tip': 0,
                'msg': '获取用户数据成功',
                'totalpage': totalpage,
                'pagenum': pagenum,
                "users": user_list,
            }
            return JsonResponse(data)

        for user in page_obj:
            user_list.append({
                'id': user.id,
                'username': user.username,
                'mobile': user.mobile,
                'type': 1,
                'email': user.email,
                'create_time': user.create_time,
                'mg_state': user.mg_state,
                'role_name': user.role_name
            })

        data = {
            'tip': 0,
            'msg': '获取用户数据成功',
            'totalpage': totalpage,
            'pagenum': pagenum,
            "users": user_list,
        }
        return JsonResponse(data)
    if request.method == 'POST':
        body_json = request.body
        body = json.loads(body_json)
        username = body.get('username', '')
        password = body.get('password', '')
        email = body.get('email', '')
        mobile = body.get('mobile', '')
        password = make_password(password)
        user = AccountUser(username=username, password=password, email=email, mobile=mobile, role_name='主管').save()
        data = {
            'tip': 0,
            'msg': '用户创建成功',
        }
        return JsonResponse(data)


def change_user_type(request):
    if request.method == 'GET':
        id = request.GET.get('uid', '')
        type = request.GET.get('type', '')
        if type == 'true':
            type = True
        else:
            type = False
        if not id or (type == None):
            data = {
                'tip': -1,
                'msg': '获取用户或参数失败',
                'data': {}
            }
            return JsonResponse(data)
        user = AccountUser.objects.filter(id=id)
        if not user:
            data = {
                'tip': -1,
                'msg': '未找到该用户',
                'data': {}
            }
            return JsonResponse(data)
        user = user.first()
        user.mg_state = type
        user.save()
        data = {
            'tip': 0,
            'msg': '修改成功',
            'data': {
                'id': user.id,
                'username': user.username,
                'mobile': user.mobile,
                'type': 1,
                'email': user.email,
                'create_time': user.create_time,
                'mg_state': user.mg_state,
                'role_name': user.role_name
            }
        }
        return JsonResponse(data)


def edit_users(request):
    if request.method == 'POST':
        body_json = request.body
        body = json.loads(body_json)
        id = body.get('id', '')
        mobile = body.get('mobile', '')
        email = body.get('email', '')
        create_time = datetime.datetime.now()
        user = AccountUser.objects.filter(id=id)
        if not user:
            data = {
                'tip': -1,
                'msg': '修改用户失败',
                'data': {}
            }
            return JsonResponse(data)
        user = user.first()
        user.mobile = mobile
        user.email = email
        user.create_time = create_time
        user.save()
        data = {
            'tip': 0,
            'msg': '修改用户成功',
            'data': {}
        }
        return JsonResponse(data)
