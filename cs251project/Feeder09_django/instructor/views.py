from django.shortcuts import render
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from myadmin.models import *
import csv
from django.views.decorators.cache import cache_control
import json
from django.views.decorators.csrf import csrf_exempt


def isInstructor(username):
    if username[0] == "i":          #REMOVE LATER
        return True
    return False


@login_required(login_url='/login/')
def home(request):
    if isInstructor(request.user.username):
        all_courses = Course.objects.all()
        context = {'all_courses': all_courses}
        return render(request, "instructor/home.html", context)
    return HttpResponse("Permission Denied - You are not an instructor")


@login_required(login_url='/login/')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def mylogout(request):
    if isInstructor(request.user.username):
        logout(request)
        return HttpResponseRedirect("/login/")
    return HttpResponse("Permission Denied - You are not an instructor")


@login_required(login_url='/login/')
def deadlines(request):
    if isInstructor(request.user.username):
        if request.method == "POST":
            curr_deadline = request.POST["deadline"]
            curr_deadline = curr_deadline.split(";&%")
            this_course = Course.objects.get(course_number=curr_deadline[0], year=curr_deadline[1],
                                             time_of_year=curr_deadline[2])
            this_deadline = Deadline.objects.get(course=this_course, deadline_description=curr_deadline[3],
                                                 deadline_dateTime=curr_deadline[4])
            context = {"deadline": this_deadline}
            return render(request, "instructor/edit_deadline.html", context)
        else:
            sorted_deadlines = Deadline.objects.order_by('-deadline_dateTime')
            context = {"all_deadlines": sorted_deadlines}
            return render(request, "instructor/deadlines.html", context)
    return HttpResponse("Permission Denied - You are not an instructor")


@login_required(login_url='/login/')
def remove_deadline(request):
    if isInstructor(request.user.username):
        if request.method == "POST":
            curr_deadline = request.POST["deadline"]
            curr_deadline = curr_deadline.split(";&%")
            this_course = Course.objects.get(course_number=curr_deadline[0], year=curr_deadline[1], time_of_year=curr_deadline[2])
            this_deadline = Deadline.objects.get(course=this_course, deadline_description=curr_deadline[3], deadline_dateTime=curr_deadline[4])
            this_deadline.delete()
        return HttpResponseRedirect("/instructor/deadlines/")
    return HttpResponse("Permission Denied - You are not an instructor")


@login_required(login_url='/login/')
def edit_deadline(request):
    if isInstructor(request.user.username):
        if request.method == "POST":
            curr_deadline = request.POST["deadline"]
            curr_deadline = curr_deadline.split(";&%")
            this_course = Course.objects.get(course_number=curr_deadline[0], year=curr_deadline[1], time_of_year=curr_deadline[2])
            this_deadline = Deadline.objects.get(course=this_course, deadline_description=curr_deadline[3], deadline_dateTime=curr_deadline[4])
            description = request.POST["description"]
            date = request.POST["date"]
            time = request.POST["time"]
            this_deadline.deadline_description = description
            this_deadline.deadline_dateTime = date+" "+time
            this_deadline.save()
        return HttpResponseRedirect("/instructor/deadlines/")
    return HttpResponse("Permission Denied - You are not an instructor")


@login_required(login_url='/login/')
def add_deadline(request):
    if isInstructor(request.user.username):
        if request.method == "POST":
            course_number = request.POST["course_number"]
            time_of_year = request.POST["optionsRadios"]
            year = request.POST["year"]
            try:
                checkcourse = Course.objects.get(course_number=course_number, year=year, time_of_year=time_of_year)
                description = request.POST["description"]
                date = request.POST["date"]
                time = request.POST["time"]
                if Deadline.objects.filter(deadline_description=description, course=checkcourse).exists():
                    return HttpResponse("Deadline already exists. Please provide a different name")
                dateTime = date+" "+time
                this_deadline = Deadline(deadline_description=description, course=checkcourse,deadline_dateTime=dateTime)
                this_deadline.save()
                return HttpResponseRedirect("/instructor/deadlines/")
            except Course.DoesNotExist:
                return HttpResponse("Course does not exist")
        else:
            all_courses = Course.objects.all()
            context = {"all_courses": all_courses}
            return render(request, "instructor/add_deadline.html", context)
    return HttpResponse("Permission Denied - You are an not instructor")


@login_required(login_url='/login/')
def feedbacks(request):
    if isInstructor(request.user.username):
        sorted_feedbacks = FeedbackForm.objects.order_by('-feedback_dateTime')
        context = {"all_feedbacks": sorted_feedbacks}
        return render(request, "instructor/feedbacks.html", context)
    return HttpResponse("Permission Denied - You are not an instructor")


@login_required(login_url='/login/')
def edit_feedback(request):
    if isInstructor(request.user.username):
        if request.method == "POST":
            curr_feedback = request.POST["feedback"]
            curr_feedback = curr_feedback.split(";&%")
            this_course = Course.objects.get(course_number=curr_feedback[0], year=curr_feedback[1], time_of_year=curr_feedback[2])
            this_feedback = FeedbackForm.objects.get(course=this_course,description=curr_feedback[3], feedback_dateTime=curr_feedback[4])
            ques = request.POST["question"]
            newquestion = Question(ques_value=ques,ques_type="radio",feedback_form=this_feedback)

            # date = request.POST["date"]
            # time = request.POST["time"]
            # this_feedback.deadline_description = description
            # this_deadline.deadline_dateTime = date+" "+time
            newquestion.save()

            this_course = Course.objects.get(course_number=curr_feedback[0], year=curr_feedback[1],
                                             time_of_year=curr_feedback[2])
            this_form = FeedbackForm.objects.get(course=this_course, description=curr_feedback[3],
                                                 feedback_dateTime=curr_feedback[4])
            context = {"feedback": this_form}
            return render(request, "instructor/edit_feedback.html", context)
        else:
            HttpResponse("Permission Denied")
    return HttpResponse("Permission Denied - You are not an instructor")


@login_required(login_url='/login/')
def remove_feedback(request):
    if isInstructor(request.user.username):
        if request.method == "POST":
            curr_feedback = request.POST["feedback"]
            curr_feedback = curr_feedback.split(";&%")
            this_course = Course.objects.get(course_number=curr_feedback[0], year=curr_feedback[1], time_of_year=curr_feedback[2])
            try:
                this_feedback = FeedbackForm.objects.get(course=this_course, description=curr_feedback[3], feedback_dateTime=curr_feedback[4])
                this_feedback.delete()
            except FeedbackForm.DoesNotExist:
                return HttpResponse("form does not exist")
        return HttpResponseRedirect("/instructor/feedbacks/")
    return HttpResponse("Permission Denied - You are not an instructor")


@login_required(login_url='/login/')
def add_feedback(request):
    if isInstructor(request.user.username):
        if request.method == "POST":
            course_number = request.POST["course_number"]
            time_of_year = request.POST["optionsRadios"]
            year = request.POST["year"]
            try:
                checkcourse = Course.objects.get(course_number=course_number, year=year, time_of_year=time_of_year)
                form_description = request.POST["description"]
                submission_date = request.POST["submission_date"]
                submission_time = request.POST["submission_time"]
                if FeedbackForm.objects.filter(description=form_description, course=checkcourse).exists():
                    return HttpResponse("Feedback form already exists. Please provide a different name")
                dateTime = submission_date+" "+submission_time
                this_form = FeedbackForm(description=form_description, course=checkcourse,feedback_dateTime=dateTime)
                this_form.save()
                return HttpResponseRedirect("/instructor/home/")
            except Course.DoesNotExist:
                return HttpResponse("Course does not exist")
        else:   
            all_courses = Course.objects.all()
            context = {"all_courses": all_courses}
            return render(request, "instructor/add_feedback.html", context)
    return HttpResponse("Permission Denied - You are an not instructor")


@login_required(login_url='/login/')
def editques_feedback(request):
    if isInstructor(request.user.username):
        if request.method == "POST":
            curr_feedback = request.POST["feedback"]
            curr_feedback = curr_feedback.split(";&%")
            this_course = Course.objects.get(course_number=curr_feedback[0], year=curr_feedback[1],
                                             time_of_year=curr_feedback[2])
            this_form = FeedbackForm.objects.get(course=this_course, description=curr_feedback[3],
                                                 feedback_dateTime=curr_feedback[4])
            context = {"feedback": this_form}
            return render(request, "instructor/edit_feedback.html", context)
        return HttpResponse("Permission Denied")
    return HttpResponse("Permission Denied - You are an not instructor")




