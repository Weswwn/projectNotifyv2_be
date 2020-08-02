from projectNotifyv2_be.celery import app
from course.models import UserCourses, Course
from user.models import User
from requests import get
from bs4 import BeautifulSoup

@app.task(bind=True)
def check_courses(self):
    listOfCourseIds = UserCourses.objects.values('course').distinct()

    for course in listOfCourseIds:
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

            notify_users(course['course'])


def notify_users(course_id):
    print('hi')
    user_obj = UserCourses.objects.values('user_id', 'id').filter(course_id=course_id)
    print(user_obj)