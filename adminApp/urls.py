from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.loginForm, name="loginForm"),
    url(r'^welcome/$', views.welcome, name="welcome"),
    url(r'^addCourse/$', views.addCourse, name="addCourse"),
    url(r'^welcome/(?P<course_number>[\d\D]+)/', views.coursePage, name="coursePage"),
    url(r'^welcome/enroll', views.enroll, name="coursePage"),
    url(r'^logout_admin', views.logout_admin, name="logout_admin"),


]