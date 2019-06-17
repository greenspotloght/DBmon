from django.conf.urls import url
from django.contrib.auth import views as auth_views
from application import views

app_name = "application"

urlpatterns = [
    url(r"dbinfo/$", views.DBInfo.as_view(), name="dbinfo"),
    url(r"dbinfo/tbspace/$", views.tbspace_chart.as_view(), name="tbspace"),
    url(r"dbinfo/sga/$", views.sga_chart.as_view(), name="sga"),
    url(r"dbinfo/pga/$", views.pga_chart.as_view(), name="pga"),
    url(r"dbinfo/dbsize/$", views.dbsize_chart.as_view(), name="dbsize"),
    url(r"dbinfo/session/$", views.session_chart.as_view(), name="session"),

    url(r"RatioInfo/$", views.Ratio.as_view(), name="ratio"),

    url(r"Perf/$", views.Perf.as_view(), name="perf"),

]
