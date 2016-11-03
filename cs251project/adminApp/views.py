from django.shortcuts import render
from django.http import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login, logout
from .models import *
from django.core.exceptions import ObjectDoesNotExist
import csv
import json
from django.views.decorators.csrf import csrf_exempt

def loginForm(request):
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
    if request.user.is_superuser:
        with open("adminApp/students.csv", 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                myrollno = row[0]
                myname = row[0]
                mypassword = row[0]
                myemail = row[3]
                if (not student.objects.filter(roll_number=myrollno).exists()) and (not User.objects.filter(username=myname).exists()):
                    newUser = User.objects.create_user(myname, myemail, mypassword)
                    newUser.save()
                    newStudent = student(roll_number=myrollno, user=newUser)
                    newStudent.save()
        all_courses = course.objects.all()
        context = {'all_courses': all_courses}
        return render(request, 'adminApp/welcome.html', context)
    return HttpResponse("Permission Denied - You are not admin")


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


def deadlineform(request, course_number):
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
    coursecurrent = course.objects.get(course_number=course_number)
    context ={"course": coursecurrent, 'endques': coursecurrent.endsemquestion_set.all(), 'midques': coursecurrent.midsemquestion_set.all()}
    return render(request,"adminApp/feedback.html",context)


def mid_feedback(request):
    if request.POST:
        coursenumber = request.POST['course_num']
        currcourse = course.objects.get(course_number=coursenumber)
        allques = currcourse.midsemquestion_set.all()
        q1 = request.POST['q1']
        q2 = request.POST['q2']
        if allques.count() == 0:
            myques = midsemquestion(ques=q1)
            myques.course = currcourse
            myques.save()
            myques = midsemquestion(ques=q2)
            myques.course = currcourse
            myques.save()
            currcourse.save()
        else:
            myq = midsemquestion.objects.get(ques=allques[0])
            myq.ques = q1
            myq.save()
            myq = midsemquestion.objects.get(ques=allques[1])
            myq.ques = q2
            myq.save()
    return HttpResponseRedirect("/adminApp/feedbackform/"+coursenumber)


def end_feedback(request):
    if request.POST:
        coursenumber = request.POST['course_num']
        currcourse = course.objects.get(course_number=coursenumber)
        allques = currcourse.endsemquestion_set.all()
        q1 = request.POST['q1']
        q2 = request.POST['q2']
        if allques.count() == 0:
            myques = endsemquestion(ques=q1)
            myques.course = currcourse
            myques.save()
            myques = endsemquestion(ques=q2)
            myques.course = currcourse
            myques.save()
            currcourse.save()
        else:
            myq = endsemquestion.objects.get(ques=allques[0])
            myq.ques = q1
            myq.save()
            myq = endsemquestion.objects.get(ques=allques[1])
            myq.ques = q2
            myq.save()

    return HttpResponseRedirect("/adminApp/feedbackform/"+coursenumber)


@csrf_exempt
def loginApp(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body.decode("utf-8"))
        username = received_json_data["username"]
        mypassword = received_json_data["pass"]
        print(username)
        print(mypassword)
        user = authenticate(username=username, password=mypassword)
        if user is not None:
            authenticated = True
        else:
            authenticated = False
        return StreamingHttpResponse(json.dumps(authenticated), content_type="application/json")
    return HttpResponse("bad username/password")



