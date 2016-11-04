from django.shortcuts import render
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
import csv
import json
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
    return HttpResponseRedirect("/login")


def login_main(request):
    if request.user.is_authenticated:
        if isAdmin(request.user.username):
            return HttpResponseRedirect("/admin/home")
        elif isInstructor(request.user.username):
            return HttpResponseRedirect("/admin/home")                     # CHANGE LATER
        else:
            return HttpResponse("Please logout of superuser first")
    if request.POST:
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
    # if user is not None:
    #     if user.is_active:
    #         login(request, user)
    #         return HttpResponseRedirect("/admin/home")
    return render(request, "main/login.html")

