from django.db import models

class course(models.Model):
    course_name = models.CharField(max_length=50)
    course_number = models.CharField(max_length=20)

    def __str__(self):
        return self.course_number