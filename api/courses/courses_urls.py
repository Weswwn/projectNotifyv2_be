from django.conf.urls import url
from api.courses.courses import CourseList, UserCourse

urlpatterns = [
    url(r'^$', CourseList.as_view()),
    url(r'^usercourse/$', UserCourse.as_view())
]
