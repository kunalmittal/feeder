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
    
    url(r'^feedbacks/$', views.feedbacks, name="feedbacks"),
    url(r'^feedbacks/remove/$', views.remove_feedback, name="remove_feedback"),
    url(r'^feedbacks/edit/$', views.edit_feedback, name="edit_feedback"),
    url(r'^add_feedback/$', views.add_feedback, name="add_feedback"),
    url(r'^feedbacks/editques/$', views.editques_feedback, name="editques_feedback"),
    url(r'^feedbacks/response/$', views.response_feedback, name="response_feedback"),

]