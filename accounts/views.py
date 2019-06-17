from django.shortcuts import render, render_to_response, Http404
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth

from django import forms
from sendmail import sendmail

from accounts.models import User_Verify, company_admin, company_user

import string
import random
import datetime

# Verify generator
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# Create your views here.
class Signup(CreateView):
    from accounts.forms import CompanyAdminForm, UserRegForm, Login
    from django.contrib.auth.forms import UserCreationForm

    form_class = CompanyAdminForm
    second_form_class = UserCreationForm
    third_form_class = UserRegForm
    forth_form_class = Login
    template_name = 'accounts/login.html'


    def get_success_url(self):
        # self.person_id = plan.person_id
        return reverse('accounts:verification')

    def get_context_data(self, **kwargs):
        expir_initial = {'date_expiration':str((datetime.datetime.today()+datetime.timedelta(days=365)).date()), 'is_active':1}
        context = {}
        if 'form' not in context:
            context['form'] = self.form_class(initial = expir_initial)
        if 'form2' not in context:
            context['form2'] = self.second_form_class
        if 'form3' not in context:
            context['form3'] = self.third_form_class
        if 'form4' not in context:
            context['form4'] = self.forth_form_class
        return context

    def get(self, request, **kwargs):
        """
        Render the forms.
        """
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        form3 = self.third_form_class(request.POST)
        form4 = self.forth_form_class(request.POST)

        if form.is_valid() and form2.is_valid() and form3.is_valid():
            username=request.POST.get('username', '')
            firstname=request.POST.get('firstname', '')
            lastname=request.POST.get('lastname', '')
            email=request.POST.get('Email', '')

            company = form.save() ##儲存公司資訊
            user = form2.save() ##儲存使用者資訊

            ###儲存使用者之姓名及信箱
            request.session['username']=username

            authuser = User.objects.get(username=username)
            authuser_id = authuser.id
            authuser.first_name=firstname
            authuser.last_name=lastname
            authuser.email=email
            authuser.is_active=1
            authuser.save()

            ###儲存公司之管理者資訊
            company_id=request.POST.get('company_id', '')
            company_info = company_admin.objects.get(company_id = company_id)
            company_info_id = company_info.id
            company_info.principal_id = authuser_id
            company_info.save()

            ###儲存公司之使用者
            companyuser = company_user.objects.create(username = username, company_admin_id = company_info_id, user_id = authuser_id)
            companyuser.save()

            ###儲存使用者之信箱認證資訊
            captcha=id_generator()
            user_verify = User_Verify.objects.create(user_id=authuser_id, captcha=captcha, is_verify=0)
            user_verify.save()



            ###寄送驗證碼
            sendmail('Verification', 'Hello, '+authuser.username+'!\nEnter '+captcha+' to verify your account.\nThank you!\n', [authuser.email])

            return HttpResponseRedirect(self.get_success_url())

        if form4.is_valid():
            username=request.POST.get('UserName','')
            password=request.POST.get('PassWord','')
            request.session['username']=username
            request.session['temp']=0
            ###登入,驗證帳號密碼
            user=auth.authenticate(username=username,password=password)
            print(user)
            if user is not None:
                try:
                    user_verify = User_Verify.objects.get(user__username=username)
                    com_is_active = company_user.objects.get(user=user.id).company_admin.is_active
                    date_expiration = company_user.objects.get(user=user.id).company_admin.date_expiration
                except Exception as e:
                    print(e)
                ###如果是一般使用者
                if user.is_superuser == 0:
                    ###檢查公司帳號啟用狀態
                    if com_is_active == 1:
                        ###檢查公司帳號是否到期
                        if date_expiration >= datetime.datetime.today().date():
                            ###檢查使用者帳號啟用狀態及使用者是否經過驗證
                            if user.is_active==1 and user_verify.is_verify==1:
                                auth.login(request,user)
                                return HttpResponseRedirect(reverse('home'))
                            elif user.is_active==1 and user_verify.is_verify==0:
                                return HttpResponseRedirect('/accounts/verification/')
                        else:
                            message = '您的註冊公司有效期限已到期'

                    else:
                        message = '您的註冊公司已停用'

                ###如果是超級使用者
                else:
                    if user.is_active==1:
                        auth.login(request,user)
                        return HttpResponseRedirect(reverse('home'))
            else:
                message = '帳號或密碼輸入錯誤'
            return render(request, self.template_name, locals())


        return render(request, self.template_name, locals())



#############################驗證###############################
def verification(request):
    from accounts.models import User_Verify
    from accounts.forms import UserVerify, UserVerify_re

    try:
        template_name = 'accounts/verification.html'
        userinfo = User.objects.get(username=request.session['username'])
        user_verify = User_Verify.objects.get(user=userinfo.id)
        if user_verify.is_verify==1:
            return HttpResponseRedirect(reverse('login'))
    except Exception as e:
        print(e)
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'POST':
        form = UserVerify(request.POST)
        form2 = UserVerify_re(request.POST)
        if request.POST.get('captcha','')==user_verify.captcha:
            user_verify.is_verify=1
            user_verify.save()
            message='Verification successfully!You can login now.'
            notify=True

            return HttpResponseRedirect(reverse('login'))

        elif form2.is_valid():
            email = form2.cleaned_data['email']
            userinfo.email = email
            userinfo.save()

            try:
                user_verify = User_Verify.objects.get(user__username=request.session['username'])
                user_verify.captcha=id_generator()

                user_verify.save()


                ###寄送驗證碼
                sendmail('Verification', 'Hello, '+user_verify.user.username+'!\nEnter '+user_verify.captcha+' to verify your account.\nThank you!\n', [user_verify.user.email])

                return HttpResponseRedirect(reverse('accounts:verification'))
            except Exception as e:
                print(e)
                raise Http404("Oops!")


    else:
        form = UserVerify()
        form2 = UserVerify_re(initial={'email':userinfo.email})
    return render(request, template_name, locals())

#############################再次寄送驗證碼###############################
def send_verification(request):
    from users.models import User_Verify
    import string
    import random

    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    try:
        user_verify = User_Verify.objects.get(user__username=request.session['username'])
        user_verify.captcha=id_generator()

        user_verify.save()


        ###寄送驗證碼
        sendmail('Verification', 'Hello, '+user_verify.user.username+'!\nEnter '+user_verify.captcha+' to verify your account.\nThank you!\n', [user_verify.user.email])

        return HttpResponseRedirect('/accounts/verification/')
    except Exception as e:
        print(e)
        raise Http404("Oops!")
################################################################




############################登入################################
# def login(request):
#     from accounts.forms import Login
#     from accounts.models import User_Verify, company_user
#
#
#     template_name = 'accounts/login.html'
#     ###檢查user是否登入,是->直接進入dashboard頁面;不是->進入登入畫面
#     if request.user.is_authenticated():
#         return HttpResponseRedirect('/')
#
#     ###如果表單提交
#     if request.method=='POST':
#         form = Login(request.POST)
#         ###檢查表單內容是否有效
#         if form.is_valid():
#             username=request.POST.get('UserName','')
#             password=request.POST.get('PassWord','')
#             request.session['username']=username
#             ###登入,驗證帳號密碼
#             user=auth.authenticate(username=username,password=password)
#             if user is not None:
#                 try:
#                     user_verify = User_Verify.objects.get(user__username=username)
#                     com_is_active = company_user.objects.get(user=user.id).company_admin.is_active
#                     date_expiration = company_user.objects.get(user=user.id).company_admin.date_expiration
#                 except Exception as e:
#                     print(e)
#                 ###如果是一般使用者
#                 if user.is_superuser == 0:
#                     ###檢查公司帳號啟用狀態
#                     if com_is_active == 1:
#                         ###檢查公司帳號是否到期
#                         if date_expiration >= datetime.datetime.today().date():
#                             ###檢查使用者帳號啟用狀態及使用者是否經過驗證
#                             if user.is_active==1 and user_verify.is_verify==1:
#                                 auth.login(request,user)
#                                 return HttpResponseRedirect('/')
#                             elif user.is_active==1 and user_verify.is_verify==0:
#                                 return HttpResponseRedirect('/accounts/verification/')
#                         else:
#                             message = '您的註冊公司有效期限已到期'
#
#                     else:
#                         message = '您的註冊公司已停用'
#
#                 ###如果是超級使用者
#                 else:
#                     if user.is_active==1:
#                         auth.login(request,user)
#                         return HttpResponseRedirect('/')
#             else:
#                 message = '帳號或密碼輸入錯誤'
#             return render(request, template_name, {'form': form, 'message':message})
#     else:
#         form = Login()
#
#     return render(request, template_name, {'form': form})
################################################################
#
# #############################登出###############################
# @login_required
# def logout(request):
#     try:
#         auth.logout(request)
#         return HttpResponseRedirect('/accounts/login/')
#     except Exception as e:
#         print(e)
#         raise Http404("Page does not exist")
# ################################################################


#############################忘記密碼###############################
def forgot_password(request):
    from accounts.forms import ForgotPswForm
    from django.contrib.auth.models import User
    import string
    import random
    template_name = 'accounts/forgot_password.html'
    message = ''
    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    if request.method == 'POST':
        form = ForgotPswForm(request.POST)
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')

        try:
            ###撈出該user資訊
            user = User.objects.get(username = username)
            try:
                ###確認email無誤
                if user.email == email:
                    ###更改密碼(6位亂碼)
                    password = id_generator()
                    user.set_password(password)
                    user.save()

                    ###寄送新密碼
                    sendmail('Reset Password', 'Hello, '+username+'!\nYour new password is '+password+'.\nYou can login with this password now.\nRemember to change your password after login successfully.\nThank you!\n', [email])
                    notify=True


                    return HttpResponseRedirect(reverse('login'))
                else:
                    message = '錯誤的信箱'
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)
            message = '無效的使用者名稱'
    else:
        form = ForgotPswForm()

    return render(request, template_name, locals())
################################################################

#############################更換密碼###############################
@login_required
def reset_password(request):
    from accounts.forms import ChangePswForm
    template_name = 'accounts/changepsw.html'
    if request.session['temp'] == '1':
        return HttpResponseRedirect('/?temp=1')

    if request.user.is_authenticated():
        user_id=request.user.id
        superuser=request.user.is_superuser
        user=request.user.username
        if superuser == 0:
            company_id = company_user.objects.get(user_id=user_id).company_admin_id
            company_ip = company_admin.objects.get(id=company_id).company_ip
        else:
            company_ip = ''
        try:
            company = company_admin.objects.get(principal=user_id)
            principal = True
        except Exception as e:
            print(e)

    if request.method=='POST':
        form=ChangePswForm(request.POST.copy())
        if form.is_valid():
            current = form.cleaned_data['current']
            new = form.cleaned_data['new']
            retype = form.cleaned_data['retype']
            ###驗證原有密碼
            usercom = auth.authenticate(username=user,password=current)

            if usercom:#原密碼正確
                if new==retype:
                    usercom.set_password(new)
                    usercom.save()
                    message='成功變更密碼!'
                    newpsw=True

                    return HttpResponseRedirect(reverse('login'))
                else:
                    message='新密碼不相符'
            else:
                if new==retype:
                    message='錯誤的舊密碼'
                else:
                    message='錯誤的舊密碼且新密碼不相符'

            return render(request, template_name, locals())
    else:
        form=ChangePswForm()

    return render(request, template_name, locals())
################################################################





#####################temp pass############################################################
def temp_login(request):
    from accounts.forms import Temp_Login
    from accounts.models import temp_pass

    template_name = 'accounts/temp_login.html'
    ###檢查user是否登入,是->直接進入dashboard頁面;不是->進入登入畫面
    if request.user.is_authenticated():
        return HttpResponseRedirect('/?temp=1')

    ###如果表單提交
    if request.method=='POST':
        form = Temp_Login(request.POST)
        ###檢查表單內容是否有效
        if form.is_valid():
            temp=request.POST.get('Temp_PassWord','')
            request.session['temp']=temp
            user = temp_pass.objects.filter(temp=temp)
            user = user[0].user
            user = User.objects.filter(username=user)
            user = user[0]
            use_temp = 1
            ###登入,驗證帳號密碼
            if user is not None:
                try:
                    user_verify = User_Verify.objects.get(user__username=user.username)
                    com_is_active = company_user.objects.get(user=user.id).company_admin.is_active
                    date_expiration = company_user.objects.get(user=user.id).company_admin.date_expiration
                except Exception as e:
                    print(e)
                ###如果是一般使用者
                if user.is_superuser == 0:
                    ###檢查公司帳號啟用狀態
                    if com_is_active == 1:
                        ###檢查公司帳號是否到期
                        if date_expiration >= datetime.datetime.today().date():
                            ###檢查使用者帳號啟用狀態及使用者是否經過驗證
                            if user.is_active==1 and user_verify.is_verify==1:
                                auth.login(request,user)
                                return HttpResponseRedirect('/?temp=1')
                            elif user.is_active==1 and user_verify.is_verify==0:
                                return HttpResponseRedirect('/accounts/verification/')
                        else:
                            message = '您的註冊公司有效期限已到期'

                    else:
                        message = '您的註冊公司已停用'

                ###如果是超級使用者
                else:
                    if user.is_active==1:
                        auth.login(request,user)
                        return HttpResponseRedirect('/')
            else:
                message = '帳號或密碼輸入錯誤'

    else:
        form = Temp_Login()

    return render(request, template_name, locals())
