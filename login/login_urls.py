#!/usr/bin/env python
# -*- coding  : utf-8 -*-
# description :
# @Time       : 2018/12/9 20:54
# @Author     : lupeng
# @File       : login_url.py
# @Software   : PyCharm

from . import views as v
from django.conf.urls import url
from django.urls import path

urlpatterns = [
    path('index/',v.index),
    path('login/', v.login),
    path('register/',v.register),
    path('logout/',v.logout),
    path('confirm/',v.useremailcfr)

]