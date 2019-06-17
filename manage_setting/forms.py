from django import forms
from django.forms import ModelForm, TextInput
from django.contrib.auth.models import User


from accounts.models import company_user
from manage_setting.models import machine_manage

###########manage user############################
class UserInfoForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class UserLineForm(ModelForm):
    class Meta:
        model = company_user
        fields = ['line_user_id']
#################################################


####################manage machine##################
class MachineInfo(ModelForm):
    hostname = forms.CharField()


    class Meta:
        model = machine_manage
        fields = '__all__'
        widgets = {
            'report_time': forms.TimeInput(attrs={'type':'time'}),
        }
