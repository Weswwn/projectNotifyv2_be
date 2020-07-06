from django.db import models


# Create your models here.
class User(models.Model):
    phone_number = models.CharField(max_length=10, blank=False, null=False)
    courses = models.ManyToManyField('course.Course', through='course.UserCourses')