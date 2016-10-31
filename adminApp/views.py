from django.shortcuts import render
from django.http import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from .models import *

def loginForm(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        if username=='admin1' and password=='admin1':
            return HttpResponseRedirect("adminApp/welcome")
    return render(request, 'adminApp/loginForm.html')

def welcome(request):
    all_courses = course.objects.all()
    context = {'all_courses' : all_courses}
    return render(request, 'adminApp/welcome.html',context)

def addCourse(request):
    if request.POST:
        coursename = request.POST['courseName']
        coursenumber = request.POST['courseNumber']
        if coursename=="" or coursenumber=="":
            return HttpResponseRedirect("/adminApp/welcome")
        newCourse = course(course_name = coursename,course_number = coursenumber)
        newCourse.save()
    return HttpResponseRedirect("/adminApp/welcome")


