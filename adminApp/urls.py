from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.loginForm, name="loginForm"),
    url(r'^welcome/$', views.welcome, name="welcome"),
    url(r'^addCourse/$', views.addCourse, name="addCourse"),

]