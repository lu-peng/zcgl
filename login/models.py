from django.db import models

# Create your models here.


class User(models.Model):
    gender=(
        ('male','男'),
        ('fmale','女')
    )
    # 用户名
    # 密码
    # 邮箱地址
    # 性别
    # 创建时间
    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256,)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=20,choices=gender,default='男')
    c_time = models.DateTimeField(auto_now_add=True)
    has_confirmed = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-c_time']
        verbose_name = '用户'
        verbose_name_plural='用户'

#创建邮件确认注册表

class UserEmailConfirm(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User',on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.name+':'+self.code
    class Meta:
        ordering = ['-c_time']
        verbose_name = '确认码'
        verbose_name_plural = '确认码'