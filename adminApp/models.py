from django.db import models
from django.contrib.auth.models import User

class course(models.Model):
    course_name = models.CharField(max_length=50)
    course_number = models.CharField(max_length=20)

    def __str__(self):
        return self.course_number

class student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=50)
    courses = models.ManyToManyField('course')

    def __str__(self):
        return self.roll_number

class question(models.Model):
	ques = models.CharField(max_length=1000)
	midsem = models.ManyToManyField('midsem')
	endsem = models.ManyToManyField('endsem')

class midsem(models.Model):
	start = models.CharField(max_length=100)
	end = models.CharField(max_length=100)
	courses = models.OneToOneField('course',on_delete=models.CASCADE)

class endsem(models.Model):
	start = models.CharField(max_length=100)
	end = models.CharField(max_length=100)
	courses = models.OneToOneField('course',on_delete=models.CASCADE)	




