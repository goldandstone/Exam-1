#_*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from django.shortcuts import render,HttpResponse
from django.contrib.auth import authenticate,login #验证登录
from django.contrib.auth.backends import ModelBackend #认证
from django.views.generic.base import View
# from captcha.models import CaptchaStore
# from captcha.helpers import captcha_image_url

import  json

from .models import UserProfile
from .forms import LoginForm
import xadmin


# class CustomBackend(ModelBackend): #定义其他字段可以登录
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         try: #根据用户名来查询是否存在
#             user = UserProfile.objects.get(username=username) #get方法得到一个用户
#             if user.check_password(password):#传输明文明码后得到暗码
#                 return  user
#         except Exception as e: #异常抛出None
#             return None


class LoginView(View):
    def get(self,request):
        login_form = LoginForm()
        captcha = login_form['captcha']
        return render(request, "exam/login.html",{'captcha':captcha})
    def post(self,request):
        login_form = LoginForm(request.POST)#声明实例化,
        captcha = login_form['captcha']
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)  # 向数据库验证，必须使用username,password来登录
            if user is not None:
                login(request, user)
                if user.role == 's':
                    userRole = ['student']
                    # userRole = "student"
                    # return HttpResponse(json.dumps({"userRole":userRole}))
                else :
                    userRole = ['teacher']
                    # userRole = "teacher"
                    # return HttpResponse(json.dumps({"userRole":userRole}))
                # return render(request, "exam/index.html")
                user_info = UserProfile.objects.get(username=user_name)
                return render(request, "exam/index.html", {"user_info": user_info,'userRole': json.dumps(userRole)})
        else:
            return render(request, "exam/login.html", {'captcha':captcha,"msg": "用户名或密码错误！"})




# Create your views here.
# def user_login(request):
#     if request.method == "POST": #判断请求方式
#         user_name = request.POST.get("username","")
#         pass_word = request.POST.get("password","")
#         user = authenticate(username=user_name,password=pass_word) #向数据库验证，必须使用username,password来登录
#         if user is not None:
#             login(request,user)
#             return render(request,"index.html")
#         else:
#             return render(request,"login.html",{"msg":"用户名或密码错误！"})
#     elif request.method == "GET":
#         return  render(request,"login.html",{})

