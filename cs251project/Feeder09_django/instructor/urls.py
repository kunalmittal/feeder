from django.conf.urls import url
from . import views

urlpatterns = [
    # all start with /instructor/


    url(r'^deadlines/$', views.deadlines, name="deadlines"),
    url(r'^home/$', views.home, name="home"),
    url(r'^logout/$', views.mylogout, name="logout"),
    url(r'^deadlines/remove/$', views.remove_deadline, name="remove_deadline"),
    url(r'^deadlines/edit/$', views.edit_deadline, name="edit_deadline"),
    url(r'^add_deadline/$', views.add_deadline, name="add_deadline"),

]