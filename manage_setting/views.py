from django.shortcuts import render, render_to_response, HttpResponseRedirect, Http404, get_object_or_404
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms

from accounts.models import company_admin, company_user
from manage_setting.models import machine_manage

from sendmail import sendmail
from db import MyMongo

# Create your views here.
# def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))

######## parent class ##########





#############################使用者管理###############################
@login_required
def user_manage(request):
    from accounts.models import company_user
    principal = False
    template_name = 'manage_setting/user/user_manage.html'
    if request.session['temp'] == '1':
        return HttpResponseRedirect('/?temp=1')
    if request.user.is_authenticated():
        user_id = request.user.id
        superuser=request.user.is_superuser
        try:
            company = company_admin.objects.get(principal=user_id)
            company_user = company_user.objects.filter(company_admin_id=company.id)
            cid = company.company_id
            #dbname = 'cid_%s'%str(cid).zfill(8)
            principal = True
        except Exception as e:
            print(e)
            raise Http404("Page does not exist")

    return render(request, template_name, locals())
################################################################

#############################新增使用者###############################
@login_required
def user_manage_add(request):
    from accounts.models import User_Verify, company_user
    from django.contrib.auth.forms import UserCreationForm
    from accounts.forms import UserRegForm

    import smtplib
    import string
    import random

    template_name = 'manage_setting/user/user_manage_add.html'
    principal = False


    if request.session['temp'] == '1':
        return HttpResponseRedirect('/?temp=1')

    if request.user.is_authenticated():
        user_id = request.user.id
        superuser=request.user.is_superuser
        try:
            company = company_admin.objects.get(principal=user_id)
            cid = company.company_id
            #dbname = 'cid_%s'%str(cid).zfill(8)
            principal = True
        except Exception as e:
            print(e)
            raise Http404("Page does not exist")

        ###提交表單
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            form1 = UserRegForm(request.POST)
            if form.is_valid() and form1.is_valid():
                form.save()
                username = request.POST.get('username','')
                first_name = request.POST.get('firstname', '')
                last_name = request.POST.get('lastname', '')
                email = request.POST.get('Email', '')
                is_active = '1'
                line = ''
                values = (username, first_name, last_name, email, is_active, line)
                #manage_setting_insert(dbname, 'auth_user', values)

                authuser = User.objects.get(username=username)
                authuser_id = authuser.id
                authuser.first_name=request.POST.get('firstname', '')
                authuser.last_name=request.POST.get('lastname', '')
                authuser.email=request.POST.get('Email', '')
                authuser.is_active=1
                authuser.save()

                companyuser = company_user.objects.create(username = username, company_admin_id = company.id, user_id = authuser_id)
                companyuser.save()

                captcha=id_generator()
                user_verify = User_Verify.objects.create(user_id=authuser_id, captcha=captcha, is_verify=0)
                user_verify.save()


                ###寄送驗證碼
                sendmail('Verification', 'Hello, '+authuser.username+'!\nEnter '+captcha+' to verify your account.\nThank you!\n', [authuser.email])

                return HttpResponseRedirect(reverse('manage_setting:user_manage'))
        else:
            form = UserCreationForm()
            form1 = UserRegForm()
    return render(request, template_name, locals())
################################################################

#############################編輯使用者###############################
@login_required
def user_manage_edit(request):
    from manage_setting.forms import UserInfoForm, UserLineForm
    #from manage_setting.manage_setting_sql import manage_setting_update,manage_setting_select_by_column
    template_name = 'manage_setting/user/user_manage_edit.html'

    if request.session['temp'] == '1':
        return HttpResponseRedirect('/?temp=1')

    if request.user.is_authenticated():
        user_id = request.user.id
        superuser=request.user.is_superuser
        try:
            company = company_admin.objects.get(principal=user_id)
            cid = company.company_id
            #dbname = 'cid_%s'%str(cid).zfill(8)
            principal = True
        except Exception as e:
            print(e)
            raise Http404("Page does not exist")

        if request.method == 'POST':
            if request.GET.get('username','')!='':
                username = request.GET.get('username','')
                user_edit = User.objects.get(username=username)
                company_user_id = company_user.objects.get(user__id = user_edit.id)
                form = UserInfoForm(request.POST, instance=user_edit)
                form1 = UserLineForm(request.POST, instance=company_user_id)
                if form.is_valid() and form1.is_valid():

                    id = User.objects.get(username=username)
                    # print(id.id)
                    username = request.POST.get('username','')
                    first_name = request.POST.get('first_name', '')
                    last_name = request.POST.get('last_name', '')
                    email = request.POST.get('Email', '')
                    line = request.POST.get('line_user_id')
                    is_active = '1'
                    values = (id, username, first_name, last_name, email, is_active, line)
                    User.objects.filter(id = id.id).update(id = id.id, username = username, first_name = first_name, last_name = last_name,
                                                                        email = email, is_active = is_active)
                    company_user.objects.filter(user_id = id.id).update(line_user_id = line)

                    #manage_setting_update(dbname, 'auth_user', values)
                    form.save()
                    form1.save()
                return HttpResponseRedirect(reverse('manage_setting:user_manage'))
        else:
            if request.GET.get('username','')!='':
                username = request.GET.get('username','')
                user_edit = User.objects.get(username=username)
                company_user_id = company_user.objects.get(user__id = user_edit.id)
                form = UserInfoForm(instance=user_edit)
                form1 = UserLineForm(instance=company_user_id)
    return render(request, template_name, locals())
################################################################

#############################刪除使用者###############################
@login_required
def user_manage_del(request):
    #from manage_setting.manage_setting_sql import manage_setting_delete_by_column

    if request.session['temp'] == '1':
        return HttpResponseRedirect('/?temp=1')

    if request.user.is_authenticated():
        user_id = request.user.id
        superuser=request.user.is_superuser
        try:
            company = company_admin.objects.get(principal=user_id)
            cid = company.company_id
            #dbname = 'cid_%s'%str(cid).zfill(8)
            principal = True
        except Exception as e:
            print(e)
            raise Http404("Page does not exist")

        if request.GET.get('username','')!='':
            username = request.GET.get('username', '')
            #manage_setting_delete_by_column(dbname, 'auth_user', 'username', username)
            username = request.GET.get('username','')
            user_del = User.objects.get(username=username)
            user_del.delete()

    return HttpResponseRedirect(reverse('manage_setting:user_manage'))
################################################################

#############################編輯公司資訊###############################
@login_required
def company_edit(request):
    from accounts.forms import CompanyAdminForm
    template_name = 'manage_setting/user/company_edit.html'

    if request.session['temp'] == '1':
        return HttpResponseRedirect('/?temp=1')

    if request.user.is_authenticated():
        user_id = request.user.id
        superuser=request.user.is_superuser
        try:
            company = company_admin.objects.get(principal=user_id)
            cid = company.company_id
            #dbname = 'cid_%s'%str(cid).zfill(8)
            principal = True
        except Exception as e:
            print(e)
            raise Http404('Page does not exist')

        if request.method == 'POST':
            form = CompanyAdminForm(request.POST, instance=company)
            if form.is_valid():
                form.save()
            return HttpResponseRedirect(reverse('manage_setting:user_manage'))
        else:
            form = CompanyAdminForm(instance=company)
            form.fields['date_expiration'].widget = forms.HiddenInput()
            form.fields['is_active'].widget = forms.HiddenInput()
            form.fields['company_id'].widget.attrs['readonly'] = True

    return render(request, template_name, locals())
################################################################



#############################使用者管理###############################
@login_required
def mc_manage(request):

    principal = False
    template_name = 'manage_setting/machine/mc_manage.html'
    if request.session['temp'] == '1':
        return HttpResponseRedirect('/?temp=1')
    if request.user.is_authenticated():
        user_id = request.user.id
        superuser=request.user.is_superuser
        try:
            company = company_admin.objects.get(principal=user_id)
            mc = machine_manage.objects.filter(company_id=company.id)
            cid = company.company_id
            #dbname = 'cid_%s'%str(cid).zfill(8)
            principal = True
        except Exception as e:
            print(e)
            raise Http404("Page does not exist")

    return render(request, template_name, locals())
################################################################

#############################新增使用者###############################
@login_required
def mc_manage_add(request):
    from manage_setting.forms import MachineInfo
    from django import forms

    template_name = 'manage_setting/machine/mc_manage_add.html'
    principal = False

    if request.session['temp'] == '1':
        return HttpResponseRedirect('/?temp=1')

    if request.user.is_authenticated():
        user_id = request.user.id
        superuser=request.user.is_superuser
        try:
            company = company_admin.objects.get(principal=user_id)
            cid = company.company_id
            dbname = 'cid_%s'%str(cid).zfill(8)
            principal = True
        except Exception as e:
            print(e)
            raise Http404("Page does not exist")

        ###提交表單
        if request.method == 'POST':
            form = MachineInfo(request.POST)

            if form.is_valid():
                form.save()

                return HttpResponseRedirect(reverse('manage_setting:mc_manage'))
        else:
            with MyMongo(database=dbname) as conn:
                host_list=conn.query_one('dbmon_Dbinfo', 'host_name')

            form = MachineInfo(initial = {'company':company_admin.objects.get(principal=user_id)})
            # set choice for choice field
            # form.fields['hostname'].choices = [(i,i) for i in host_list]
            form.fields['hostname'].widget=forms.Select(choices=[(i,i) for i in host_list])
            form.fields['company'].widget.attrs['disabled'] = True



    return render(request, template_name, locals())
################################################################


#############################編輯使用者###############################
@login_required
def mc_manage_edit(request):
    from manage_setting.forms import MachineInfo
    from django import forms

    template_name = 'manage_setting/machine/mc_manage_edit.html'

    if request.session['temp'] == '1':
        return HttpResponseRedirect('/?temp=1')

    if request.user.is_authenticated():
        user_id = request.user.id
        superuser=request.user.is_superuser
        try:
            company = company_admin.objects.get(principal=user_id)
            cid = company.company_id
            #dbname = 'cid_%s'%str(cid).zfill(8)
            principal = True
        except Exception as e:
            print(e)
            raise Http404("Page does not exist")

        if request.method == 'POST':
            if request.GET.get('hostname','')!='':
                hostname = request.GET.get('hostname','')
                ip = request.GET.get('ip','')
                mc_edit = machine_manage.objects.get(hostname=hostname, ip=ip)
                form = MachineInfo(request.POST, instance=mc_edit)

                if form.is_valid():
                    form.save()

                return HttpResponseRedirect(reverse('manage_setting:mc_manage'))
        else:
            if request.GET.get('hostname','')!='':
                hostname = request.GET.get('hostname','')
                ip = request.GET.get('ip','')
                mc_edit = machine_manage.objects.get(hostname=hostname, ip=ip)
                form = MachineInfo(instance=mc_edit)

    return render(request, template_name, locals())
################################################################

#############################remove machine###############################
@login_required
def mc_manage_del(request):


    if request.session['temp'] == '1':
        return HttpResponseRedirect('/?temp=1')

    if request.user.is_authenticated():
        user_id = request.user.id
        superuser=request.user.is_superuser
        try:
            company = company_admin.objects.get(principal=user_id)
            cid = company.company_id
            #dbname = 'cid_%s'%str(cid).zfill(8)
            principal = True
        except Exception as e:
            print(e)
            raise Http404("Page does not exist")

        if request.GET.get('hostname','')!='':
            hostname = request.GET.get('hostname', '')
            ip = request.GET.get('ip','')
            host_del = machine_manage.objects.get(hostname=hostname,ip=ip)
            host_del.delete()

    return HttpResponseRedirect(reverse('manage_setting:mc_manage'))
################################################################
