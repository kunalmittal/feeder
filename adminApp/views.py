from django.shortcuts import render
from django.http import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login, logout
from .models import *
from django.core.exceptions import ObjectDoesNotExist
import csv


def loginForm(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("welcome")
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("welcome")

        if username == 'admin1' and password == 'admin1':
            return HttpResponseRedirect("welcome")

    return render(request, 'adminApp/loginForm.html')


@login_required(login_url='/adminApp/')
def welcome(request):
    with open("adminApp/students.csv", 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            myrollno = row[0]
            myname = row[1]
            if (not student.objects.filter(roll_number=myrollno).exists()) and (not User.objects.filter(username=myname).exists()):
                newUser = User(username=myname)
                newUser.save()
                newStudent = student(roll_number=myrollno, user=newUser)
                newStudent.save()
    all_courses = course.objects.all()
    context = {'all_courses': all_courses}
    return render(request, 'adminApp/welcome.html', context)


def addCourse(request):
    if request.POST:
        coursename = request.POST['courseName']
        coursenumber = request.POST['courseNumber']
        if coursename=="" or coursenumber=="":
            return HttpResponseRedirect("/adminApp/welcome")
        newCourse = course(course_name = coursename,course_number = coursenumber)
        newCourse.save()
    return HttpResponseRedirect("/adminApp/welcome")


def coursePage(request,course_number):
    all_students = student.objects.all()
    context = {"course_number": course_number, "all_students": all_students}
    return render(request,"adminApp/coursePage.html", context)


def enroll(request):
    if request.POST:
        selectedStudents = request.POST.getlist('selected')
        coursenumber = request.POST['course_num']
        currCourse = course.objects.get(course_number=coursenumber)
        for curr_pk in selectedStudents:
            student.objects.get(pk=curr_pk).courses.add(currCourse)
    return HttpResponseRedirect("/adminApp/welcome")


def logout_admin(request):
    logout(request)
    return HttpResponseRedirect('/adminApp/')


def deadlineform(request,course_number):
    thiscourse = course.objects.get(course_number=course_number)
    context ={"course": thiscourse}
    return render(request,"adminApp/deadline.html", context)


def mid_deadline(request):
    if request.POST:
        coursenumber = request.POST['course_num']
        currcourse = course.objects.get(course_number=coursenumber)
        formdate = request.POST['midDate']
        currcourse.mid_deadline = formdate
        currcourse.save()
    return HttpResponseRedirect("/adminApp/deadlineform/"+coursenumber)


def end_deadline(request):
    if request.POST:
        coursenumber = request.POST['course_num']
        currcourse = course.objects.get(course_number=coursenumber)
        formdate = request.POST['endDate']
        currcourse.end_deadline = formdate
        currcourse.save()
    return HttpResponseRedirect("/adminApp/deadlineform/"+coursenumber)


def feedbackform(request,course_number):
    context ={"course_number": course_number}
    return render(request,"adminApp/feedback.html",context)


def mid_feedback(request):
    if request.POST:
        coursenumber = request.POST['course_num']
        currcourse = course.objects.get(course_number=coursenumber)
        q1 = request.POST['q1']
        q2 = request.POST['q2']
        myques = midsemquestion(ques=q1)
        myques.course = currcourse
        myques.save()
        myques = midsemquestion(ques=q2)
        myques.course = currcourse
        myques.save()
        currcourse.save()
    return HttpResponseRedirect("/adminApp/feedbackform/"+coursenumber)


def end_feedback(request):
    if request.POST:
        coursenumber = request.POST['course_num']
        currcourse = course.objects.get(course_number=coursenumber)
        q1 = request.POST['q1']
        q2 = request.POST['q2']
        myques = endsemquestion(ques=q1)
        myques.course = currcourse
        myques.save()
        myques = endsemquestion(ques=q2)
        myques.course = currcourse
        myques.save()
        currcourse.save()
    return HttpResponseRedirect("/adminApp/feedbackform/"+coursenumber)

