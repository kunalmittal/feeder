from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$', views.login_init, name="login_init"),
    url(r'^login/$', views.login_main, name="login_main"),
    url(r'^register/$', views.register, name="register"),
    url(r'^fb/register/$', views.fblogin, name="fblogin"),

]