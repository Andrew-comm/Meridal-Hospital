from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from patients.models import Patient

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

    user = request.user

    total_users = User.objects.count()

    # Patient stats
    total_patients = Patient.objects.count()
    recent_patients = Patient.objects.order_by("-created_at")[:5]

    # ROLE FLAGS (IMPORTANT FOR UI CONTROL)
    role = user.role

    context = {
        "current_user": user,
        "total_users": total_users,
        "total_patients": total_patients,
        "recent_patients": recent_patients,
        "role": role,

        # Permissions for UI
        "can_create_patient": role in ["ADMIN", "RECEPTIONIST"],
        "can_view_patients": role in ["ADMIN", "RECEPTIONIST", "DOCTOR", "NURSE", "LAB_TECH", "PHARMACIST"],
        "can_manage_users": role == "ADMIN",
    }

    return render(request, "dashboard.html", context)


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
