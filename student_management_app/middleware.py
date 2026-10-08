from django.shortcuts import redirect


class RoleBasedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        # Public pages
        public_paths = [
            "/",
            "/doLogin/",
            "/logout_user/",
        ]

        if path in public_paths:
            return self.get_response(request)

        # Not logged in
        if not request.user.is_authenticated:
            return redirect("login")

        user_type = str(request.user.user_type)

        # Staff-only URLs
        staff_paths = [
            "/staff_home/",
            "/staff_take_attendance/",
            "/get_students/",
            "/save_attendance_data/",
            "/staff_update_attendance/",
            "/get_attendance_dates/",
            "/get_attendance_student/",
            "/update_attendance_data/",
            "/staff_apply_leave/",
            "/staff_apply_leave_save/",
            "/staff_feedback/",
            "/staff_feedback_save/",
            "/staff_profile/",
            "/staff_profile_update/",
            "/staff_add_result/",
            "/staff_add_result_save/",
        ]

        # Student-only URLs
        student_paths = [
            "/student_home/",
            "/student_view_attendance/",
            "/student_view_attendance_post/",
            "/student_apply_leave/",
            "/student_apply_leave_save/",
            "/student_feedback/",
            "/student_feedback_save/",
            "/student_profile/",
            "/student_profile_update/",
            "/student_view_result/",
            "/student_fee_history/",
        ]

        # HOD URLs
        hod_prefixes = [
            "/admin_home/",
            "/add_staff/",
            "/manage_staff/",
            "/edit_staff/",
            "/delete_staff/",
            "/add_course/",
            "/manage_course/",
            "/edit_course/",
            "/delete_course/",
            "/manage_session/",
            "/add_session/",
            "/edit_session/",
            "/delete_session/",
            "/add_student/",
            "/manage_student/",
            "/edit_student/",
            "/delete_student/",
            "/manage_fee/",
            "/edit_fee/",
            "/delete_fee/",
            "/add_subject/",
            "/manage_subject/",
            "/edit_subject/",
            "/delete_subject/",
            "/admin_view_attendance/",
            "/admin_profile/",
        ]

        # Staff access check
        if any(path.startswith(p) for p in staff_paths):
            if user_type != "2":
                return self.redirect_to_own_dashboard(user_type)

        # Student access check
        if any(path.startswith(p) for p in student_paths):
            if user_type != "3":
                return self.redirect_to_own_dashboard(user_type)

        # HOD access check
        if any(path.startswith(p) for p in hod_prefixes):
            if user_type != "1":
                return self.redirect_to_own_dashboard(user_type)

        return self.get_response(request)

    def redirect_to_own_dashboard(self, user_type):
        if user_type == "1":
            return redirect("admin_home")
        elif user_type == "2":
            return redirect("staff_home")
        elif user_type == "3":
            return redirect("student_home")
        return redirect("login")