from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from accounts.models import company_admin, company_user, suggestion

########### create user forms #############
class UserRegForm(forms.Form):
    lastname=forms.CharField(required=True,label='姓(Last Name)',max_length=20)
    firstname=forms.CharField(required=True,label='名(First Name)',max_length=20)
    Email=forms.EmailField(required=True,label='E-mail',max_length=254)


class CompanyAdminForm(forms.ModelForm):

    class Meta:
        model = company_admin
        exclude = ['principal','company_db']
        widgets = {
            'company_ip': forms.TextInput(attrs={'placeholder': '255.255.255.255'}),
            'company_ip2': forms.TextInput(attrs={'placeholder': '255.255.255.255', 'required': False}),
            'company_ip3': forms.TextInput(attrs={'placeholder': '255.255.255.255', 'required': False}),
            'date_expiration': forms.HiddenInput(),
            'is_active': forms.HiddenInput(),

        }

# veriication
class UserVerify(forms.Form):
    captcha=forms.CharField(required=True, label='請輸入認證碼',max_length=6)

# veriication
class UserVerify_re(forms.Form):
    email=forms.EmailField(required=True,label='E-mail',max_length=254)




##############################################################################


class Login(forms.Form):
    UserName=forms.CharField(max_length=30)
    PassWord=forms.CharField(label='Password', widget=forms.PasswordInput)


class ChangePswForm(forms.Form):
    current = forms.CharField(label='請輸入舊密碼',max_length=30,widget=forms.PasswordInput(attrs={'size':20,}))
    new = forms.CharField(label='請輸入新密碼',max_length=30,widget=forms.PasswordInput(attrs={'size':20,}))
    retype = forms.CharField(label='請再次輸入新密碼',max_length=30,widget=forms.PasswordInput(attrs={'size':20}))


class Login(forms.Form):
    UserName=forms.CharField(max_length=30)
    PassWord=forms.CharField(label='Password', widget=forms.PasswordInput)

class ForgotPswForm(forms.Form):
    username=forms.CharField(max_length=30,label='UserName')
    email=forms.EmailField(required=True,label='E-mail',max_length=254)


class Temp_Login(forms.Form):
    Temp_PassWord=forms.CharField(label='Temp_Password', widget=forms.PasswordInput)
