from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from . import views
from django.http import HttpResponse
from django.contrib import messages


# Create your views here.
def Register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        account_type = request.POST.get("account_type")

        # check if passwords match
        if password1 != password2:
            error_message = "passwords does not match. please use a common password"
            return render(
                request,
                "authentication/register.html",
                {"error_message": error_message},
            )

        # check if username already exists
        if User.objects.filter(username=username).exists():
            error_message = "The user exists. please login!"
            return render(
                request,
                "authentication/register.html",
                {"error_message": error_message},
            )

        # check if the email is already reister to another account
        if User.objects.filter(email=email).exists():
            error_message = "the email address is registered to another account"
            return render(
                request,
                "authentication/register.html",
                {"error_message": error_message},
            )

        # create the user
        new_user = User.objects.create_user(
            username=username, email=email, password=password1
        )
        new_user.first_name = full_name
        
        # assign role
        if account_type == "employee":
            new_user.is_staff = True
        else:
            new_user.is_staff = False
            
        new_user.save()

        messages.success(request, "The Account successsfully Create")
        return redirect("authentication:login")
    return render(request, "authentication/register.html", {})


def Login(request):
    error_message = None
    if request.method == "POST":
        username = request.POST.get("fname")
        password = request.POST.get("pwd")
        role = request.POST.get("role", "user")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Enforce role selection for login
            if role == "employee" and not (user.is_staff or user.is_superuser):
                error_message = "This account is not registered as a Farmer. Please login as a Customer."
            elif role == "user" and user.is_staff and not user.is_superuser:
                error_message = "This account is registered as a Farmer. Please login using the Farmer tab."
            else:
                login(request, user)
                return redirect("homepage:mainpage")

        else:
            error_message = "Invalid username or password. Please try again."

    return render(
        request, "authentication/login.html", {"error_message": error_message}
    )

def Logout(request):
    logout(request)
    return redirect("authentication:login")


def ForgotPassword(request):
    if request.method == "POST":
        email = request.POST.get("email")
        messages.success(request, f"If {email} is registered, a password reset link has been sent!")
        return redirect("authentication:login")
    return render(request, "authentication/forgot_password.html", {})
