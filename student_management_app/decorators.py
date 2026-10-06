from django.shortcuts import redirect


def hod_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if str(request.user.user_type) != '1':
            if str(request.user.user_type) == '2':
                return redirect('staff_home')
            elif str(request.user.user_type) == '3':
                return redirect('student_home')
            return redirect('login')

        return view_func(request, *args, **kwargs)

    return wrapper


def staff_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if str(request.user.user_type) != '2':
            if str(request.user.user_type) == '1':
                return redirect('admin_home')
            elif str(request.user.user_type) == '3':
                return redirect('student_home')
            return redirect('login')

        return view_func(request, *args, **kwargs)

    return wrapper