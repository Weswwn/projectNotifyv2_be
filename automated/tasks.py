from projectNotifyv2_be.celery import app
from course.models import UserCourses, Course
from user.models import User
from requests import get
from bs4 import BeautifulSoup
from twilio.rest import Client
from projectNotifyv2_be.secret import TWILIO_ACCT_SID, TWILIO_AUTH_TOKEN, TWILIO_TEST_SID, TWILIO_TEST_AUTH
import asyncio


@app.task(bind=True)
def check_courses(self):
    list_of_course_id = UserCourses.objects.values('course').filter(did_text_send=False).distinct()
    print(list_of_course_id)
    for course in list_of_course_id:
        course_obj = Course.objects.get(id=course['course'])

        subject_code = course_obj.subject_code
        subject_number = course_obj.subject_number
        section_number = course_obj.section_number

        url = f"https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-section&dept={subject_code}&course={subject_number}&section={section_number}"

        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        type(html_soup)

        general_seat_div = html_soup.find_all(string='General Seats Remaining:')

        """ ------ IMPORTANT ------
        At this point, need to add another course validation check. If a course is valid during form input,
        but changes later, this portion of the code will now catch this issue.
            ------ IMPORTANT ------ """
        if len(general_seat_div) > 0:
            general_seat_count = general_seat_div[0].findParent().findNextSibling().text

            if int(general_seat_count) >= 0:
                notify_users(course['course'], subject_code, subject_number, section_number)


def notify_users(course_id, subject_code, subject_number, section_number):
    # Once a course has an opening spot query all users who have requested that course
    user_courses_list = UserCourses.objects.values('user_id', 'id').filter(course_id=course_id, did_text_send=False)
    client = Client(TWILIO_ACCT_SID, TWILIO_AUTH_TOKEN)

    # Notify each user that made registrations for the course that has an open spot
    for record in user_courses_list:
        print(record['id'])

        #Ran into an issue here where the result of the .get didn't provide the value. Look into this
        phone_number_obj = User.objects.values('phone_number').get(id=record['user_id'])
        phone_number = phone_number_obj['phone_number']
        send_sms_to_user(client, phone_number, subject_code, subject_number, section_number, record['id'])


def send_sms_to_user(client, phone_number, subject_code, subject_number, section_number, record_id):
    try:
        message = client.messages \
            .create(
                body=f"Hi! This is Project Notify. A spot for {subject_code} {subject_number} {section_number} opened up! Click the link to register: https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-section&dept={subject_code}&course={subject_number}&section={section_number}",
                from_="2017293373",
                #15005550006
                status_callback='https://83cd00628ae6.ngrok.io/api/course/usercourse/',
                to=phone_number
        )
        user_courses_record = UserCourses.objects.get(id=record_id)
        user_courses_record.sms_message_sid = message.sid
        user_courses_record.save(update_fields=['sms_message_sid'])
    except Exception as e:
        print('Sending text message has failed')