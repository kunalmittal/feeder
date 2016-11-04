from django.conf.urls import url
from . import views

urlpatterns = [
    # all start with /admin/
    url(r'^home/$', views.home, name="home"),
    url(r'^add_course/$', views.add_course, name="add_course"),
    url(r'^logout/$', views.mylogout, name="logout"),
    url(r'^load_students/$', views.load_students, name="load_students"),
    url(r'^deadlines/$', views.deadlines, name="deadlines"),
    url(r'^enroll/$', views.enroll, name="enroll"),
    url(r'^enroll/student/$', views.enroll_student, name="enroll_student"),


]