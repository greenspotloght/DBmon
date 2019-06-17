from django.conf.urls import url
from django.contrib.auth import views as auth_views
from accounts import views

app_name = "accounts"

urlpatterns = [
    url(r"^login/$", views.Signup.as_view(), name="login"),
    url(r"logout/$", auth_views.LogoutView.as_view(), name="logout"),
    #url(r"signup/$", views.Signup.as_view(), name="signup"),
    url(r"verification/$", views.verification, name="verification"),
    url(r"forgot/$", views.forgot_password, name="forgot"),
    url(r"resetpsw/$", views.reset_password, name="resetpsw"),

    url(r"templogin/$", views.temp_login, name="templogin"),
]
