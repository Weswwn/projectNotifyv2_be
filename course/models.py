from django.db import models

class Course(models.Model):
    subjectCode = models.CharField(max_length=4, blank=False, null=False)
    subjectNumber = models.CharField(max_length=4, blank=False, null=False)
    sectionNumber = models.CharField(max_length=4, blank=False, null=False)
    # users = models.ManyToManyField('user.User', through='UserCourses')

    class Meta:
        unique_together = ('subjectCode', 'subjectNumber', 'sectionNumber',)

#
# class UserCourses(models.Model):
#     user = models.ForeignKey('user.User', on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)