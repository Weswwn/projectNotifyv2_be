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

    def post(self, request, *args, **kwargs):
        subjectCode = request.data['subjectCode']
        subjectNumber = request.data['subjectNumber']
        sectionNumber = request.data['sectionNumber']
        user = request.data['users']
        course = Course.objects.filter()
