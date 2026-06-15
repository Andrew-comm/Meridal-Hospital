from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User


def login_view(request):
    """
    User Login
    """

    # If already logged in
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            messages.success(
                request,
                f"Welcome back, {user.username}!"
            )

            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "login.html"
    )


@login_required
def dashboard(request):
    """
    Dashboard View
    """

    context = {
        "total_users": User.objects.count(),
        "current_user": request.user,
    }

    return render(
        request,
        "dashboard.html",
        context
    )


@login_required
def profile(request):
    """
    User Profile
    """

    context = {
        "user": request.user
    }

    return render(
        request,
        "profile.html",
        context
    )


@login_required
def user_list(request):
    """
    View all users
    """

    users = User.objects.all().order_by("username")

    context = {
        "users": users
    }

    return render(
        request,
        "users.html",
        context
    )


@login_required
def logout_view(request):
    """
    Logout User
    """

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("login")
