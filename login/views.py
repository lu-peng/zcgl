import datetime
import hashlib
from django.shortcuts import render,redirect
import os
from zcgl import settings
from . import models
from . import forms
from django.core.mail import send_mail, EmailMultiAlternatives
# Create your views here.

def index(request):
    pass
    return render(request,'login/index.html')

# def login(request):
#     print(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'====')
#     if request.method == "POST":
#         # username = request.POST['username']
#         # password = request.POST['password']
#         username = request.POST.get('username',None)
#         password = request.POST.get('password',None)
#         message = '所有字段都必须填写！'
#         if username and password:
#             username = username.strip() #去除两端空白
#             password = password.strip()
#             print(username,password)
#             try:
#                 user = models.User.objects.get(name = username)
#                 if user.password == password:
#                     return redirect('/main/index/')
#                 else:
#                     message = '密码不正确！'
#             except :
#                 message = '用户不存在！'
#         return render(request,'login/login.html',{'message':message})
#     return render(request,'login/login.html')
#使用表单模型后的视图
def login(request):
    if request.session.get('is_login',None):
        return redirect('/main/index/')
    if request.method == "POST":
        login_form = forms.UserFrom(request.POST)
        message = '所有字段都必须填写！'
        if login_form.is_valid():
            username = login_form.cleaned_data['username'].strip() #去除两端空白
            password = login_form.cleaned_data['password'].strip()
            print(username,password)
            try:
                user = models.User.objects.get(name = username)
                if not user.has_confirmed:
                    message = '该用户还未经过邮箱确认，请确认！'
                    return render(request,'login/useremailconfirm.html',locals())
                if user.password == hash_code(password):
                    request.session['is_login']=True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/main/index/')
                else:
                    message = '密码不正确！'
            except :
                message = '用户不存在！'
        return render(request,'login/login.html',locals())
    login_form = forms.UserFrom()
    print(locals())
    return render(request,'login/login.html',locals())
def register(request):
    if request.session.get('is_login',None):
        message = '用户已经登录不能注册'
        return redirect('/main/index/')
    if request.method=='POST':
        registerForm = forms.RegisterForm(request.POST)
        message='请检查填写内容'
        if registerForm.is_valid():
            username = registerForm.cleaned_data['username'].strip()
            password1 = registerForm.cleaned_data['password1'].strip()
            password2 = registerForm.cleaned_data['password2'].strip()
            email = registerForm.cleaned_data['email'].strip()
            sex = registerForm.cleaned_data['sex'].strip()
            try:
                same_name = models.User.objects.filter(name = username)
                if same_name:
                    message = '用户已经存在，请重新输入用户！'
                    return render(request, 'login/register.html', locals())
                else:
                    if password1 != password2:
                        message="两次输入的密码不一致！"
                        render(request, 'login/register.html', locals())
                same_email = models.User.objects.filter(email=email)
                if same_email:
                    message = '邮箱已经注册，请使用别的邮箱'
                    return render(request, 'login/register.html', locals())
                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.has_confirmed=False
                new_user.save()
                code = make_confirm_hscode(new_user)
                models.UserEmailConfirm.objects.create(code=code,user=new_user)
                send_mail(code,email)
                message='注册成功！'
            except Exception as e:
                print(e)
                return render(request, 'login/register.html', locals())
            #login_form = forms.UserFrom()
            return render(request, 'login/useremailconfirm.html', locals())
    registerForm=forms.RegisterForm()
    return render(request,'login/register.html',locals())
#用户邮箱确认视图
def useremailcfr(request):
    code = request.GET.get('code',None)
    message = ''
    try:
        confirm = models.UserEmailConfirm.objects.get(code=code)
    except Exception as e:
        message = '无效的注册请求'
        return render(request,'login/useremailconfirm.html',locals())
    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        message = '您的邮件已经过期，请重新注册！'
        return render(request, 'login/useremailconfirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账号登录！'
        return render(request, 'login/useremailconfirm.html', locals())


#退出用户登录状态
def logout(request):
    if not request.session['is_login']:
        return redirect('/main/index/')
    request.session.flush()
    #或者使用下面方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect('/main/index/')


#加密

def hash_code(s,salt='zcgl'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())# update方法只接收bytes类型
    return h.hexdigest()
#生成确认码
#参数用户对象
def make_confirm_hscode(user):
    now = datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
    code = hash_code(user.name,now)
    return code
#发送邮件
def send_mail(code,email):
    print('code5===' + code)
    ##发送普通邮件
    # send_mail(
    #     '邮件主题',
    #     '邮件内容',
    #     '960232328@qq.com',
    #     ['alupeng0707@163.com'],
    # )
    # 发送HTML格式的邮件
    subject = '来自资产管理系统的注册确认邮件'

    text_content = '''感谢注册资产管理系统，如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                        <p>感谢注册<a href="http://{}/main/confirm/?code={}" target=blank>请点击链接确认注册</a></p>
                        <p>此链接有效期为{}天！</p>
                        '''.format('127.0.0.1:8080', code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()