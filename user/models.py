from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator


# Create your models here.
class User(models.Model):
    phone_number = PhoneNumberField(blank=False, null=False, validators=[RegexValidator('^\d{3}\d{3}\d{4}$')])
    courses = models.ManyToManyField('course.Course', through='course.UserCourses')

    def __str__(self):
        return str(self.phone_number)