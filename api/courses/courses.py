from rest_framework import generics
from api.courses.courses_serializers import CourseListSerializer
from course.models import Course, UserCourses
from user.models import User
from rest_framework.response import Response
from requests import get
from bs4 import BeautifulSoup


class CourseList(generics.ListCreateAPIView):
    model = Course
    def get_serializer_class(self):
        return CourseListSerializer

    def get_queryset(self):
        q_set = Course.users.through.objects.all()
        return q_set

    def post(self, request, *args, **kwargs):
        subject_code = request.data['subjectCode']
        subject_number = request.data['subjectNumber']
        section_number = request.data['sectionNumber']
        phone_number = request.data['users']
        course = Course.objects.filter(subject_code=subject_code, subject_number=subject_number, section_number=section_number)
        user = User.objects.filter(phone_number=phone_number)

        url = f"https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-section&dept={subject_code}&course={subject_number}&section={section_number}"
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        type(html_soup)
        general_seat_div = html_soup.find_all(string='General Seats Remaining:')

        if len(general_seat_div) == 0:
            return Response({'status': 'The course you requested is not valid'})

        general_seat_count = general_seat_div[0].findParent().findNextSibling().text

        if general_seat_count == '0':
            if course and user:
                # if the course already exists in the database
                # Check if record already exists in the user table

                unique_reservation = UserCourses.objects.filter(user=user[0].id, course=course[0].id)
                if unique_reservation:
                    return Response({'status': 'You have already registered for this course'})

                reservation = UserCourses(user=user[0], course=course[0])
                reservation.save()
                return Response({'status': 'Success'})

            elif not user and not course:
                user_data = User(phone_number=phone_number)
                user_data.save()
                course_data = Course(subject_code=subject_code, subject_number=subject_number, section_number=section_number)
                course_data.save()
                course_data.users.set([user_data])

                reservation = UserCourses(user=user_data, course=course_data)
                # reservation.save()
                return Response({'status': 'Success'})

            elif course and not user:
                # if the phone number does not exist in the database yet
                user_data = User(phone_number=phone_number)
                user_data.save()

                reservation = UserCourses(user=user_data, course=course[0])
                reservation.save()
                return Response({'status': 'Success'})

            elif user and not course:
                # if the course does not exist in the database yet
                course_data = Course(subject_code=subject_code, subject_number=subject_number, section_number=section_number)
                course_data.save()
                course_data.users.set([user[0]])

                reservation = UserCourses(user=user[0], course=course_data)
                # reservation.save()
                return Response({'status': 'Success'})

        return Response({'status': 'The course you requested is not full'})
