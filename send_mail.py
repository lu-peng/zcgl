#!/usr/bin/env python
# -*- coding  : utf-8 -*-
# description :
# @Time       : 2018/12/13 15:37
# @Author     : lupeng
# @File       : send_mail.py
# @Software   : PyCharm
import os
from django.core.mail import send_mail, EmailMultiAlternatives

os.environ['DJANGO_SETTINGS_MODULE'] = 'zcgl.settings'
'''
if __name__ == '__main__':
    ##发送普通邮件
    # send_mail(
    #     '邮件主题',
    #     '邮件内容',
    #     '960232328@qq.com',
    #     ['alupeng0707@163.com'],
    # )
    #发送HTML格式的邮件
    subject, from_email, to = '来自卢鹏的测试邮件', '960232328@qq.com', 'alupeng0707@163.com'
    #其中的text_content是用于当HTML内容无效时的替代txt文本。
    text_content = '欢迎访问www.liujiangblog.com，这里是刘江的博客和教程站点，专注于Python和Django技术的分享！'
    html_content = '<p>欢迎访问<a href="http://www.liujiangblog.com" target=blank>www.liujiangblog.com</a>，这里是刘江的博客和教程站点，专注于Python和Django技术的分享！</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

'''