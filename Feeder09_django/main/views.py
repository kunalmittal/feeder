from django.shortcuts import render
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from myadmin.models import *
import csv
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt


def isAdmin(username):
    if username[0] == "a":
        return True
    return False


def isInstructor(username):
    if username[0] == "i":
        return True
    return False


def login_init(request):
    return HttpResponseRedirect("/login/")


def login_main(request):
    if request.user.is_authenticated:
        if isAdmin(request.user.username):
            return HttpResponseRedirect("/admin/home")
        elif isInstructor(request.user.username):
            return HttpResponseRedirect("/instructor/home")
        #else:
                                                                           #CHANGE LATER
            #return HttpResponse("Please logout of superuser first")
    if request.method == "POST":
        username = request.POST['username']
        mypassword = request.POST['password']
        ad_or_ins = request.POST["optionsRadios"]
        if ad_or_ins == "admin":
            return login_admin(request, username, mypassword)
        else:
            return login_ins(request, username, mypassword)
    return render(request, "main/login.html")


def login_admin(request, username, mypassword):
    username = "a:"+username
    user = authenticate(username=username, password=mypassword)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect("/admin/home")
    return HttpResponse("Bad username/password")
    # return render(request, "main/login.html")


def login_ins(request, username, mypassword):
    username = "i:"+username
    user = authenticate(username=username, password=mypassword)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect("/instructor/home/")
    return HttpResponse("Bad username/password")


def register(request):
    if request.method == "POST":
        myemail = request.POST["email"]
        myemail = "i:"+myemail
        mypassword = request.POST["password"]
        name = request.POST["name"]
        if not User.objects.filter(username=myemail).exists():
            user = User.objects.create_user(username=myemail, password=mypassword, first_name=name)
            user.save()
            return HttpResponseRedirect("/login/")
        else:
            return HttpResponse("Email already registered")
    return HttpResponseRedirect("/login/")


def fblogin(request):
    if request.method == "POST":
        myemail = request.POST["email-value"]
        myname = request.POST["name-value"]
        print(myname)
        print (myemail)
        print("HI")
        try:
            user = User.objects.get(username=myemail)
            if user.is_active:
                login(request, user)
                # print(myemail)
                return HttpResponseRedirect("/instructor/home/")
        except User.DoesNotExist:
            user = User.objects.create_user(username=myemail)
            user.save()
            login(request, user)
    return HttpResponseRedirect("/login/")


@csrf_exempt
def loginApp(request):
    return HttpResponse("bad username/password")
#     if request.method == 'POST':
#         received_json_data = json.loads(request.body.decode("utf-8"))
#         username = received_json_data["username"]
#         mypassword = received_json_data["pass"]
#         username="s:"+username
#         print(username, mypassword)
#         myuser = authenticate(username=username, password=mypassword)
#         if myuser is not None:
#             student = Student.objects.get(user=myuser)
#             course_query = student.courses.all()
#             for c in course_query:

#                 s = "{\"courses\":[";
#                 for c in course_query:
#                     feed_list = c.feedbackform_set.all()
#                     ass_list = c.deadline_set.all()
#                     s = s + "{\"course_number\":\"" + str(c.course_number) + "\","
#                     # s=s+"\"course_name\":\""+str(c.course_name)+"\","
#                     # s=s+"\"course_year\":\""+str(c.course_year)+"\","
#                     # s=s+"\"course_sem\":\""+str(c.course_sem)+"\","
#                     s = s + "\"feedback_forms\":["
#                     for f in feed_list:
#                         qn_list = f.feedback_questions.all()
#                         s = s + "{\"feedback_deadline_datetime\":\"" + str(
#                             f.feedback_deadline.deadline_datetime) + "\","
#                         s = s + "\"feedback_name\":\"" + str(f.feedback_name) + "\","
#                         s = s + "\"feedback_questions\":["
#                         for q in qn_list:
#                             s = s + "{\"question_name\":\"" + str(q.question_name) + "\""
#                             s = s + "},"
#                         if qn_list:
#                             s = s[:-1]
#                         s = s + "]"
#                         s = s + "},"
#                     if feed_list:
#                         s = s[:-1]
#                     s = s + "]"
#                     s = s + ","
#                     s = s + "\"assignment_deadline\":["
#                     for a in ass_list:
#                         s = s + "{\"deadline_name\":\"" + str(a.deadline_name) + "\","
#                         s = s + "\"deadline_datetime\":\"" + str(a.deadline_datetime) + "\","
#                         s = s[:-1]
#                         s = s + "},"
#                     s = s[:-1]
#                     s = s + "]"
#                     s = s + "},"
#                 if course_query:
#                     s = s[:-1]
#                 s = s + "]}"
#             else:
#                 s = False


#             data = serializers.serialize("json", student.courses.all())
#         else:
#             data = "[{\"authenticated\": \"False\"}]"
#         return StreamingHttpResponse(data, content_type="application/json")


