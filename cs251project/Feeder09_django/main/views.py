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
        try:
            user = User.objects.get(username=myemail)
            if user.is_active:
                login(request, user)
                print(myemail)
                return HttpResponseRedirect("/instructor/home/")
            return render(request, "myadmin/enroll_in_course.html", context)
        except User.DoesNotExist:
            print(myemail)
            # user = User.objects.create_user(username=myemail)
            # user.save()
            return HttpResponse("Course does not exist")
    return HttpResponseRedirect("/login/")


@csrf_exempt
def loginApp(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body.decode("utf-8"))
        username = received_json_data["username"]
        mypassword = received_json_data["pass"]
        username="s:"+username
        print(username, mypassword)
        myuser = authenticate(username=username, password=mypassword)
        if myuser is not None:
            student = Student.objects.get(user=myuser)
            data = serializers.serialize("json", student.courses.all())
        else:
            data = "[{\"authenticated\": \"False\"}]"
        return StreamingHttpResponse(data, content_type="application/json")
    return HttpResponse("bad username/password")