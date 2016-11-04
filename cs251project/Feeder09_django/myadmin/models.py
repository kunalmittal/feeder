from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Course(models.Model):
    course_name = models.CharField(max_length=50)
    course_number = models.CharField(max_length=10)
    time_of_year = models.CharField(max_length=10)
    year = models.IntegerField()

    def __str__(self):
        return self.course_number


class Deadline(models.Model):
    deadline_description = models.CharField(max_length=100)
    deadline_dateTime = models.DateTimeField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.course.__str__()+ " "+ self.deadline_description

    @property
    def is_past_due(self):
        now = timezone.localtime(timezone.now())
        if now > self.deadline_dateTime:
            return True
        return False


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return self.user.username


class FeedbackForm(models.Model):
    desciption = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.course.__str__() +" "+ self.desciption


class Question(models.Model):
    ques_value = models.CharField(max_length=200)
    ques_type = models.CharField(max_length=10)
    feedback_form = models.ForeignKey(FeedbackForm, on_delete=models.CASCADE, null="true")

    def __str__(self):
        return self.feedback_form.__str__() +" question"


