from rest_framework import generics, status
from api.courses.courses_serializers import CourseListSerializer, UserCoursesSerializer
from course.models import Course, UserCourses
from user.models import User

from rest_framework.response import Response
from requests import get

from bs4 import BeautifulSoup

import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type


class CourseList(generics.ListCreateAPIView):
    model = Course
    def get_serializer_class(self):
        print(self.request.method)
        if self.request.method == 'GET':
            return CourseListSerializer
        else:
            return UserCoursesSerializer

    def get_queryset(self):
        q_set = Course.objects.all();
        return q_set


    def post(self, request, *args, **kwargs):
        subject_code = request.data['subjectCode']
        subject_number = request.data['subjectNumber']
        section_number = request.data['sectionNumber']
        phone_number = request.data['users']

        is_valid = validate_phonenumber(phone_number)
        if is_valid is False:
            return Response({'status': 'failed', 'msg': 'Something went wrong with your phone number'},
                     status=status.HTTP_404_NOT_FOUND)

        course = Course.objects.filter(subject_code=subject_code, subject_number=subject_number, section_number=section_number)
        user = User.objects.filter(phone_number=phone_number)

        url = f"https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-section&dept={subject_code}&course={subject_number}&section={section_number}"
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        type(html_soup)
        general_seat_div = html_soup.find_all(string='General Seats Remaining:')

        if len(general_seat_div) == 0:
            return Response({'status': 'failed', 'msg': 'The course you requested is not valid'}, status=status.HTTP_404_NOT_FOUND)

        general_seat_count = general_seat_div[0].findParent().findNextSibling().text

        if general_seat_count == '0':
            if course and user:
                print(course, user)
                # if the course and user already exist in the database
                # Check if record already exists in the user table

                unique_reservation = UserCourses.objects.filter(user=user[0].id, course=course[0].id, did_text_send=False)
                if unique_reservation:
                    return Response({'status': 'failed', 'msg': 'You have already registered for this course'}, status=status.HTTP_404_NOT_FOUND)

                reservation = UserCourses(user=user[0], course=course[0])
                reservation.save()
                return Response({'status': 'success', 'msg': 'You have been registered'})

            elif not user and not course:
                user_data = User(phone_number=phone_number)
                user_data.save()
                course_data = Course(subject_code=subject_code, subject_number=subject_number, section_number=section_number)
                course_data.save()
                course_data.users.set([user_data])

                reservation = UserCourses(user=user_data, course=course_data)
                # reservation.save()
                return Response({'status': 'success', 'msg': 'You have been registered'})

            elif course and not user:
                # if the phone number does not exist in the database yet
                user_data = User(phone_number=phone_number)
                user_data.save()

                reservation = UserCourses(user=user_data, course=course[0])
                reservation.save()
                return Response({'status': 'success', 'msg': 'You have been registered'})

            elif user and not course:
                # if the course does not exist in the database yet
                course_data = Course(subject_code=subject_code, subject_number=subject_number, section_number=section_number)
                course_data.save()
                course_data.users.set([user[0]])

                reservation = UserCourses(user=user[0], course=course_data)
                # reservation.save()
                return Response({'status': 'success', 'msg': 'You have been registered'})

        return Response({'status': 'failed', 'msg': 'The course you requested is not full'}, status=status.HTTP_404_NOT_FOUND)


class UserCourse(generics.ListCreateAPIView):

    def post(self, request, *args, **kwargs):
        print('THIS IS A BIG ASS TEST', request, request.data)
        sms_sid = request.data.get('MessageSid')
        sms_status = request.data.get('MessageStatus')
        user_course_record = UserCourses.objects.get(sms_message_sid=sms_sid)

        if sms_status == 'sent' or 'delivered':
            user_course_record.did_text_send = True
        else:
            user_course_record.did_text_send = False
        user_course_record.save(update_fields=['did_text_send'])

        return Response({'status': 'complete'})


def validate_phonenumber(phone_number):
    try:
        isValid = phonenumbers.is_possible_number(phonenumbers.parse(phone_number, None))
        print(phonenumbers.parse(phone_number, None), phonenumbers.is_possible_number(phonenumbers.parse(phone_number, None)))
    except Exception as e:
        return False

    return isValid