from course.models import Course
from rest_framework import serializers

class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            'subjectCode',
            'subjectNumber',
            'sectionNumber',
            'users'
        )