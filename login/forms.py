#!/usr/bin/env python
# -*- coding  : utf-8 -*-
# description :
# @Time       : 2018/12/10 21:03
# @Author     : lupeng
# @File       : forms.py
# @Software   : PyCharm

# 设置表单模型
from captcha.fields import CaptchaField
from django import forms


class UserFrom(forms.Form):
    username = forms.CharField(label='用户',max_length=128,widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='密码',max_length=256,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    captcha = CaptchaField(label='验证码')

class RegisterForm(forms.Form):
    gender = (
        ('male', '男'),
        ('fmale', '女')
    )
    # 用户名
    # 密码
    # 邮箱地址
    # 性别
    # 创建时间
    username = forms.CharField(max_length=128, label='用户',widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(max_length=256,label='密码',widget=forms.PasswordInput(attrs={'class':'form-control'}) )
    password2 = forms.CharField(max_length=258,label='确认密码',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='邮箱',widget=forms.EmailInput(attrs={'class':'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    captcha = CaptchaField(label='验证码')

