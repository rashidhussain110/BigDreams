from datetime import date

from django.test import TestCase
from django.urls import reverse

from student_management_app.models import CustomUser, Courses, SessionYearModel


# Pages that need no ID in the URL, grouped by who uses them.
PUBLIC_PAGES = [
    "login",
    "student_registration",
]

HOD_PAGES = [
    "admin_home",
    "add_staff",
    "manage_staff",
    "add_course",
    "manage_course",
    "manage_session",
    "add_session",
    "add_student",
    "manage_student",
    "manage_fee",
    "add_subject",
    "manage_subject",
    "student_feedback_message",
    "staff_feedback_message",
    "student_leave_view",
    "staff_leave_view",
    "admin_view_attendance",
    "admin_profile",
]

STAFF_PAGES = [
    "staff_home",
    "staff_take_attendance",
    "staff_update_attendance",
    "staff_apply_leave",
    "staff_feedback",
    "staff_profile",
    "staff_add_result",
]

STUDENT_PAGES = [
    "student_home",
    "student_view_attendance",
    "student_apply_leave",
    "student_feedback",
    "student_profile",
    "student_view_result",
]


class SmokeTest(TestCase):
    """
    Opens every page once and checks that it does not crash.
    This uses a temporary test database, so your real db.sqlite3 is never touched.
    """

    def check_pages(self, user_type, username, page_names):
        user = CustomUser.objects.create_user(
            username=username,
            password="test12345",
            email=username + "@test.com",
            first_name="Test",
            last_name="User",
            user_type=user_type,
        )
        self.client.force_login(user)

        for name in page_names:
            with self.subTest(page=name):
                response = self.client.get(reverse(name))
                # 200 = page opened, 302 = redirected (normal for some pages)
                self.assertIn(
                    response.status_code,
                    (200, 302),
                    "Page '%s' returned status %s" % (name, response.status_code),
                )

    def test_public_pages(self):
        for name in PUBLIC_PAGES:
            with self.subTest(page=name):
                response = self.client.get(reverse(name))
                self.assertIn(response.status_code, (200, 302))

    def test_hod_pages(self):
        self.check_pages(1, "smoke_hod", HOD_PAGES)

    def test_staff_pages(self):
        self.check_pages(2, "smoke_staff", STAFF_PAGES)
    
    def test_student_pages(self):
        # A real student always has a course and a session, so create them first
        course = Courses.objects.create(course_name="Test Course")
        session = SessionYearModel.objects.create(
            session_start_year=date(2026, 1, 1),
            session_end_year=date(2029, 12, 31),
        )

        user = CustomUser.objects.create_user(
            username="smoke_student",
            password="test12345",
            email="smoke_student@test.com",
            first_name="Test",
            last_name="User",
            user_type=3,
        )

        student = user.students
        student.course_id = course
        student.session_year_id = session
        student.save()

        self.client.force_login(user)

        for name in STUDENT_PAGES:
            with self.subTest(page=name):
                response = self.client.get(reverse(name))
                self.assertIn(
                    response.status_code,
                    (200, 302),
                    "Page '%s' returned status %s" % (name, response.status_code),
                )