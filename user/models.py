from django.db import models

# Create your models here.
class User(models.Model):
    phone_number = models.CharField(max_length=12, blank=False, null=False)
    courses = models.ManyToManyField('course.Course', through='course.UserCourses')

    def __str__(self):
        return str(self.phone_number)