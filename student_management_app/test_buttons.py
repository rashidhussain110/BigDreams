from datetime import date

from django.test import TestCase
from django.urls import reverse

from student_management_app.models import (
    CustomUser, Courses, SessionYearModel, Subjects, Students, StudentFee,
    Attendance, AttendanceReport, LeaveReportStudent, FeedBackStudent,
)


class ButtonTest(TestCase):
    """
    Clicks the buttons that need an ID in the link (Edit, Delete, History, Add Fee)
    and checks the main save actions. Runs on a temporary test database only.
    """

    def setUp(self):
        # HOD who is logged in for every test
        self.hod = CustomUser.objects.create_user(
            username="btn_hod", password="test12345", email="btn_hod@test.com",
            first_name="Hod", last_name="User", user_type=1,
        )
        self.client.force_login(self.hod)

        # Shared data
        self.course = Courses.objects.create(course_name="Test Course")
        self.session = SessionYearModel.objects.create(
            session_start_year=date(2026, 1, 1),
            session_end_year=date(2029, 12, 31),
        )

        # One staff member
        self.staff_user = CustomUser.objects.create_user(
            username="btn_staff", password="test12345", email="btn_staff@test.com",
            first_name="Staff", last_name="User", user_type=2,
        )

        # One subject
        self.subject = Subjects.objects.create(
            subject_name="Test Subject", course_id=self.course, staff_id=self.staff_user,
        )

        # One student with a course, a session and a first fee
        self.student_user = CustomUser.objects.create_user(
            username="btn_student", password="test12345", email="btn_student@test.com",
            first_name="Stud", last_name="Ent", user_type=3,
        )
        self.student = self.student_user.students
        self.student.course_id = self.course
        self.student.session_year_id = self.session
        self.student.save()

        self.fee = StudentFee.objects.create(
            student_id=self.student, fee_period=date(2026, 10, 1),
            total_fee=1000, paid_fee=0,
        )

    def open_page(self, url):
        response = self.client.get(url)
        self.assertIn(response.status_code, (200, 302), "%s returned %s" % (url, response.status_code))
        return response

    # ---------- Pages with an ID in the link ----------

    def test_edit_and_history_pages_open(self):
        pages = {
            "edit_staff": reverse("edit_staff", args=[self.staff_user.id]),
            "edit_course": reverse("edit_course", args=[self.course.id]),
            "edit_session": reverse("edit_session", args=[self.session.id]),
            "edit_subject": reverse("edit_subject", args=[self.subject.id]),
            "edit_student": reverse("edit_student", args=[self.student_user.id]),
            "edit_fee": reverse("edit_fee", args=[self.fee.id]),
            "fee_history": reverse("fee_history", args=[self.student.id]),
            "add_fee": reverse("add_fee", args=[self.student.id]),
        }
        for name, url in pages.items():
            with self.subTest(page=name):
                self.open_page(url)

    # ---------- Fee actions ----------

    def test_add_fee_creates_new_month_and_manage_fee_shows_latest(self):
        self.client.post(reverse("add_fee_save"), {
            "student_id": self.student.id,
            "fee_period": "2026-11-01",
            "due_date": "2026-11-10",
            "total_fee": "1000",
            "paid_fee": "500",
            "paid_date": "",
        })
        self.assertEqual(StudentFee.objects.filter(student_id=self.student).count(), 2)

        response = self.client.get(reverse("manage_fee"))
        fees = list(response.context["fees"])
        self.assertEqual(len(fees), 1)
        self.assertEqual(str(fees[0].fee_period), "2026-11-01")

    def test_edit_fee_changes_only_that_month(self):
        other = StudentFee.objects.create(
            student_id=self.student, fee_period=date(2026, 11, 1),
            total_fee=1000, paid_fee=0,
        )
        self.client.post(reverse("edit_fee_save"), {
            "fee_id": self.fee.id,
            "fee_period": "2026-10-01",
            "due_date": "",
            "total_fee": "1000",
            "paid_fee": "1000",
            "paid_date": "2026-10-05",
        })
        self.fee.refresh_from_db()
        other.refresh_from_db()
        self.assertEqual(self.fee.paid_fee, 1000)
        self.assertEqual(other.paid_fee, 0)

    # ---------- Add Student ----------

    def test_add_student_creates_first_fee(self):
        response = self.client.post(reverse("add_student_save"), {
            "first_name": "New",
            "last_name": "Student",
            "username": "new_student_x",
            "email": "new_student_x@test.com",
            "password": "test12345",
            "address": "Test address",
            "course_id": self.course.id,
            "session_year_id": self.session.id,
            "gender": "Male",
        })
        user = CustomUser.objects.filter(username="new_student_x").first()
        self.assertIsNotNone(user, "Student was not created (the form may have been rejected)")
        self.assertEqual(StudentFee.objects.filter(student_id=user.students).count(), 1)

    # ---------- Delete actions ----------

    def test_delete_student_removes_student_data_only(self):
        # Give the student some related data
        attendance = Attendance.objects.create(
            subject_id=self.subject, attendance_date=date(2026, 10, 6), session_year_id=self.session,
        )
        AttendanceReport.objects.create(student_id=self.student, attendance_id=attendance, status=True)
        LeaveReportStudent.objects.create(
            student_id=self.student, leave_date="2026-10-07", leave_message="Test", leave_status=0,
        )
        FeedBackStudent.objects.create(student_id=self.student, feedback="Test", feedback_reply="")

        # A second student who must NOT be touched
        other_user = CustomUser.objects.create_user(
            username="btn_other", password="test12345", email="btn_other@test.com", user_type=3,
        )
        other_user.students.course_id = self.course
        other_user.students.session_year_id = self.session
        other_user.students.save()

        self.client.get(reverse("delete_student", args=[self.student_user.id]))

        self.assertFalse(CustomUser.objects.filter(id=self.student_user.id).exists(), "User left behind")
        self.assertFalse(Students.objects.filter(id=self.student.id).exists(), "Students profile left behind")
        self.assertEqual(StudentFee.objects.filter(student_id=self.student.id).count(), 0, "Fees left behind")
        self.assertEqual(AttendanceReport.objects.filter(student_id=self.student.id).count(), 0, "Attendance rows left behind")
        self.assertEqual(LeaveReportStudent.objects.filter(student_id=self.student.id).count(), 0, "Leave left behind")
        self.assertEqual(FeedBackStudent.objects.filter(student_id=self.student.id).count(), 0, "Feedback left behind")

        # Shared data and other students stay
        self.assertTrue(Courses.objects.filter(id=self.course.id).exists())
        self.assertTrue(SessionYearModel.objects.filter(id=self.session.id).exists())
        self.assertTrue(CustomUser.objects.filter(id=other_user.id).exists())

    def test_delete_pages_do_not_crash(self):
        # Each delete runs on its own copy of the data (setUp runs again for every test),
        # so this test only checks that the other delete buttons open without errors.
        for name, arg in [
            ("delete_subject", self.subject.id),
            ("delete_course", self.course.id),
            ("delete_session", self.session.id),
            ("delete_staff", self.staff_user.id),
        ]:
            with self.subTest(page=name):
                response = self.client.get(reverse(name, args=[arg]))
                self.assertIn(response.status_code, (200, 302), "%s returned %s" % (name, response.status_code))