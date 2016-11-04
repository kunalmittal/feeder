from django.shortcuts import render
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from myadmin.models import *
import csv
from django.views.decorators.cache import cache_control
import json
from django.views.decorators.csrf import csrf_exempt


def isAdmin(username):
    if username[0] == "a":
        return True
    return False


@login_required(login_url='/login/')
def home(request):
    if isAdmin(request.user.username):
        all_courses = Course.objects.all()
        context = {'all_courses': all_courses}
        return render(request, "myadmin/home.html", context)
    return HttpResponse("Permission Denied - You are not admin")


@login_required(login_url='/login/')
def add_course(request):
    if isAdmin(request.user.username):
        if request.method == "POST":
            course_number = request.POST["course_number"]
            course_name = request.POST["course_name"]
            time_of_year = request.POST["optionsRadios"]
            year = request.POST["year"]
            midsem_exam = request.POST["midsem_date"]
            endsem_exam = request.POST["endsem_date"]
            checkcourse = Course.objects.filter(course_number=course_number, year=year, time_of_year=time_of_year)
            if checkcourse.exists():
                return HttpResponse("Course already exists")
            this_course = Course(course_name=course_name, course_number=course_number, time_of_year=time_of_year, year=year)
            this_course.save()
            mid_deadline = Deadline(deadline_description="Midsem Exam Date", deadline_dateTime=midsem_exam+" 23:55:00", course=this_course)
            mid_deadline.save()
            end_deadline = Deadline(deadline_description="Endsem Exam Date", deadline_dateTime=endsem_exam + " 23:55:00", course=this_course)
            end_deadline.save()
            midsem_feedback = FeedbackForm(desciption="Midsem Feedback", course=this_course)
            endsem_feedback = FeedbackForm(desciption="Endsem Feedback", course=this_course)
            midsem_feedback.save()
            endsem_feedback.save()
            midsem1 = request.POST["midsem1"]
            midsem2 = request.POST["midsem2"]
            endsem1 = request.POST["endsem1"]
            endsem2 = request.POST["endsem2"]
            midsem_q1 = Question(ques_value=midsem1, ques_type="radio", feedback_form=midsem_feedback)
            midsem_q2 = Question(ques_value=midsem2, ques_type="radio", feedback_form=midsem_feedback)
            endsem_q1 = Question(ques_value=endsem1, ques_type="radio", feedback_form=midsem_feedback)
            endsem_q2 = Question(ques_value=endsem2, ques_type="radio", feedback_form=midsem_feedback)
            midsem_q1.save()
            midsem_q2.save()
            endsem_q1.save()
            endsem_q2.save()
            return HttpResponseRedirect("/admin/home")
        return render(request, "myadmin/add_course.html")
    return HttpResponse("Permission Denied - You are not admin")


def loadall():
    with open("students.csv", 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            myrollno = row[0]
            myname = row[1]
            mypass = row[2]
            myemail = row[3]
            if not User.objects.filter(username=myrollno).exists():
                if not mypass == '':
                    newUser = User.objects.create_user(email=myemail, password=mypass, username=myrollno, first_name=myname)
                    newUser.save()
                    newStudent = Student(user=newUser)
                    newStudent.save()
    return HttpResponseRedirect("/admin/home")


@login_required(login_url='/login/')
def load_students(request):
    if isAdmin(request.user.username):
        return loadall()
    return HttpResponse("Permission Denied - You are not admin")


@login_required(login_url='/login/')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def mylogout(request):
    if isAdmin(request.user.username):
        logout(request)
        return HttpResponseRedirect("/login/")
    return HttpResponse("Permission Denied - You are not admin")


@login_required(login_url='/login/')
def deadlines(request):
    if isAdmin(request.user.username):
        sorted_deadlines = Deadline.objects.order_by('-deadline_dateTime')
        context = {"all_deadlines": sorted_deadlines}
        return render(request, "myadmin/deadlines.html", context)
    return HttpResponse("Permission Denied - You are not admin")


@login_required(login_url='/login/')
def enroll(request):
    if isAdmin(request.user.username):
        if request.method == "POST":
            course_number = request.POST["course_number"]
            time_of_year = request.POST["optionsRadios"]
            year = request.POST["year"]
            try:
                checkcourse = Course.objects.get(course_number=course_number, year=year, time_of_year=time_of_year)
                all_students_in_course = checkcourse.student_set.all()
                all_students = Student.objects.all()
                req_students = all_students.exclude(pk__in=all_students_in_course)
                context = {'all_students': req_students, "course": checkcourse}
                return render(request, "myadmin/enroll_in_course.html", context)
            except Course.DoesNotExist:
                return HttpResponse("Course does not exist")
        all_courses = Course.objects.all()
        context = {'all_courses': all_courses}
        return render(request, "myadmin/enroll.html", context)
    return HttpResponse("Permission Denied - You are not admin")


@login_required(login_url='/login/')
def enroll_student(request):
    if isAdmin(request.user.username):
        if request.method == "POST":
            course_number = request.POST["course_number"]
            time_of_year = request.POST["time_of_year"]
            year = request.POST["year"]
            checkcourse = Course.objects.get(course_number=course_number, year=year, time_of_year=time_of_year)
            selectedStudents = request.POST.getlist('student_list')
            for myusername in selectedStudents:
                myuser = User.objects.get(username=myusername)
                student = Student.objects.get(user=myuser)
                student.courses.add(checkcourse)
            return HttpResponseRedirect("/admin/enroll")
    return HttpResponse("Permission Denied - You are not admin")

