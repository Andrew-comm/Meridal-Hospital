from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from patients.models import Patient
from appointments.models import Appointment

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
    role = user.role

    # -----------------------------
    # ROLE PERMISSIONS
    # -----------------------------
    can_manage_users = role == "ADMIN"

    can_create_patient = role in ["ADMIN", "RECEPTIONIST"]
    can_view_patients = role in ["ADMIN", "RECEPTIONIST", "DOCTOR", "NURSE"]

    can_create_appointment = role in ["ADMIN", "RECEPTIONIST"]
    can_view_appointments = role in ["ADMIN", "RECEPTIONIST", "DOCTOR", "NURSE", "LAB_TECH", "PHARMACIST"]

    # -----------------------------
    # DATA COUNTS
    # -----------------------------
    total_users = User.objects.count() if can_manage_users else None
    total_patients = Patient.objects.count()
    total_appointments = Appointment.objects.count()

    # -----------------------------
    # RECENT DATA
    # -----------------------------
    recent_patients = Patient.objects.select_related(
        "registered_by"
    ).order_by("-created_at")[:5]

    recent_appointments = Appointment.objects.select_related(
        "patient", "doctor"
    ).order_by("-created_at")[:5]

    # -----------------------------
    # DOCTOR FILTER (optional future-ready)
    # -----------------------------
    doctor_appointments = None

    if role == "DOCTOR":
        doctor_appointments = Appointment.objects.filter(
            doctor=user
        ).order_by("-appointment_date")[:5]

    # -----------------------------
    # CONTEXT
    # -----------------------------
    context = {
        "role": role,
        "current_user": user,

        # permissions
        "can_manage_users": can_manage_users,
        "can_create_patient": can_create_patient,
        "can_view_patients": can_view_patients,
        "can_create_appointment": can_create_appointment,
        "can_view_appointments": can_view_appointments,

        # stats
        "total_users": total_users,
        "total_patients": total_patients,
        "total_appointments": total_appointments,

        # data
        "recent_patients": recent_patients,
        "recent_appointments": recent_appointments,
        "doctor_appointments": doctor_appointments,
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
