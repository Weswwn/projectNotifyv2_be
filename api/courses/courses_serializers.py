from course.models import Course

class CourseListSerializer():
    class Meta:
        model = Course
        fields = (
            'subjectCode',
            'subjectNumber',
            'sectionNumber',
            'user'
        )