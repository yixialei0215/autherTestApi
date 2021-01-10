import datetime

from django.db import models
from django.contrib.auth.hashers import make_password, check_password


# Create your models here.
class AccountUser(models.Model):
    username = models.CharField(max_length=20, null=True, verbose_name='用户名')
    password = models.CharField(max_length=200, null=True, verbose_name='密码')
    mobile = models.CharField(max_length=11, null=True, verbose_name='手机号')
    email = models.EmailField(null=True, verbose_name='邮箱')
    role_name = models.CharField(max_length=20, verbose_name='权限名称', null=True)
    mg_state = models.BooleanField(default=True, null=True)
    create_time = models.DateTimeField(default=datetime.datetime.now(), null=True)

    class Meta:
        verbose_name_plural = verbose_name = '用户信息'
        db_table = 'account_user'


class Menus(models.Model):
    authname = models.CharField(max_length=50, null=True, verbose_name='菜单名')
    path = models.CharField(max_length=100, null=True, verbose_name='路径')
    fatherid = models.ForeignKey('self', on_delete=models.CASCADE, null=True, verbose_name='父id')
    menu = models.ManyToManyField('AccountUser', verbose_name='菜单')

    class Meta:
        verbose_name_plural = verbose_name = '菜单栏'
        db_table = 'menus'
