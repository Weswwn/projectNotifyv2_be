from projectNotifyv2_be.celery import app
from course.models import UserCourses, Course
from user.models import User
from requests import get
from bs4 import BeautifulSoup
from twilio.rest import Client
from projectNotifyv2_be.secret import TWILIO_ACCT_SID, TWILIO_AUTH_TOKEN


@app.task(bind=True)
def check_courses(self):
    list_of_course_id = UserCourses.objects.values('course').distinct()
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
        general_seat_count = general_seat_div[0].findParent().findNextSibling().text

        if int(general_seat_count) >= 0:
            notify_users(course['course'], subject_code, subject_number, section_number)


def notify_users(course_id, subject_code, subject_number, section_number):
    # Once a course has an opening spot query all users who have requested that course
    user_list = UserCourses.objects.values('user_id', 'id').filter(course_id=course_id)
    client = Client(TWILIO_ACCT_SID, TWILIO_AUTH_TOKEN)

    # Notify each user that made registrations for the course that has an open spot
    for user in user_list:
        phone_number = User.objects.filter(id=user['user_id'])
        send_sms_to_user(client, phone_number, subject_code, subject_number, section_number)


def send_sms_to_user(client, phone_number, subject_code, subject_number, section_number):
    message = client.messages \
        .create(
            body=f"Hi! This is Project Notify. A spot for {subject_code} {subject_number} {section_number} opened up! Click the link to register: https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-section&dept={subject_code}&course={subject_number}&section={section_number}",
            from_="+12017293373",
            to=phone_number
    )
    print(message.sid)
