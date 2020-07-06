from rest_framework import generics
from api.courses.courses_serializers import CourseListSerializer


class CourseList(generics.ListCreateAPIView):

    def get_serializer_class(self):
        return CourseListSerializer