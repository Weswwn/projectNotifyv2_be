from django.db import models

class Course(models.Model):
    subject_code = models.CharField(max_length=4, blank=False, null=False)
    subject_number = models.CharField(max_length=4, blank=False, null=False)
    section_number = models.CharField(max_length=4, blank=False, null=False)
    users = models.ManyToManyField('user.User', through='UserCourses')

    class Meta:
        unique_together = ('subject_code', 'subject_number', 'section_number',)

    def __str__(self):
        return self.subject_code + self.subject_number + self.section_number


class UserCourses(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)