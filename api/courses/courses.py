from rest_framework import generics
from api.courses.courses_serializers import CourseListSerializer
from course.models import Course


class CourseList(generics.ListCreateAPIView):
    model = Course
    def get_serializer_class(self):
        return CourseListSerializer

    def get_queryset(self):
        q_set = Course.objects.all()
        return q_set
