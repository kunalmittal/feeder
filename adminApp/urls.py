from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.loginForm, name="loginForm"),
    url(r'^welcome/$', views.welcome, name="welcome"),
    url(r'^addCourse/$', views.addCourse, name="addCourse"),
    url(r'^feedbackform/(?P<course_number>[\d\D]+)/',views.feedbackform,name="feedback"),
    url(r'^deadlineform/(?P<course_number>[\d\D]+)/',views.deadlineform,name="deadline"),
    url(r'^welcome/(?P<course_number>[\d\D]+)/', views.coursePage, name="coursePage"),
    url(r'^welcome/enroll', views.enroll, name="coursePage"),
    url(r'^mid_feedback/$',views.mid_feedback,name="mid_feedback"),
    url(r'^end_feedback/$',views.end_feedback,name="end_feedback"),
    url(r'^mid_deadline/$',views.mid_deadline,name="mid_deadline"),
    url(r'^end_deadline/$',views.end_deadline,name="end_deadline"),
    url(r'^logout_admin/$', views.logout_admin, name="logout_admin"),


]