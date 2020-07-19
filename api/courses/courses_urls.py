from django.conf.urls import url
from api.courses.courses import CourseList

urlpatterns = [
    url(r'^$', CourseList.as_view()),
]
