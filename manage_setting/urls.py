from django.conf.urls import url
from django.contrib.auth import views as auth_views
from manage_setting import views

app_name = "manage_setting"

urlpatterns = [
    url(r"company/$", views.user_manage, name='user_manage'),
    url(r"company/edit/$", views.company_edit, name='company_edit'),
    url(r"user/add/$", views.user_manage_add, name='user_add'),
    url(r"user/del/$", views.user_manage_del, name='user_del'),
    url(r"user/edit/$", views.user_manage_edit, name='user_edit'),

    url(r"machine/$", views.mc_manage, name='mc_manage'),
    url(r"machine/add/$", views.mc_manage_add, name='mc_add'),
    url(r"machine/edit/$", views.mc_manage_edit, name='mc_edit'),
    url(r"machine/del/$", views.mc_manage_del, name='mc_del'),
]
