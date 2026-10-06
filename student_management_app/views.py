# from channels.auth import login, logout
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from student_management_app.EmailBackEnd import EmailBackEnd


def home(request):
    return render(request, 'index.html')


def loginPage(request):
    host = request.get_host().split(':')[0].lower()

    if host == "hod.localhost":
        return render(request, "login.html", {"login_role": "HOD"})

    elif host == "staff.localhost":
        return render(request, "login.html", {"login_role": "Staff"})

    elif host == "student.localhost":
        return render(request, "login.html", {"login_role": "Student"})

    return render(request, "login.html", {"login_role": "Normal"})


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")

    login_role = request.POST.get("login_role")

    user = EmailBackEnd.authenticate(
        request,
        username=request.POST.get("email"),
        password=request.POST.get("password")
    )

    if user != None:

        user_type = str(user.user_type)

        # Check that the user is logging in from the correct role URL
        if login_role == "HOD" and user_type != "1":
            messages.error(request, "This account is not an HOD account.")
            return redirect("login")

        if login_role == "Staff" and user_type != "2":
            messages.error(request, "This account is not a Staff account.")
            return redirect("login")

        if login_role == "Student" and user_type != "3":
            messages.error(request, "This account is not a Student account.")
            return redirect("login")

        login(request, user)

        if user_type == "1":
            return redirect("admin_home")

        elif user_type == "2":
            return redirect("staff_home")

        elif user_type == "3":
            return redirect("student_home")

        else:
            messages.error(request, "Invalid Login!")
            return redirect("login")

    else:
        messages.error(request, "Invalid Login Credentials!")
        return redirect("login")


def get_user_details(request):
    if request.user != None:
        return HttpResponse("User: "+request.user.email+" User Type: "+request.user.user_type)
    else:
        return HttpResponse("Please Login First")



def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


