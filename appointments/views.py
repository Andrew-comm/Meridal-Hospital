from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from Accounts.decorators import role_required

from .models import Appointment
from .forms import AppointmentForm


@login_required
@role_required([
    "ADMIN",
    "RECEPTIONIST",
    "DOCTOR",
    "NURSE"
])
def appointment_list(request):

    if request.user.role == "DOCTOR":

        appointments = Appointment.objects.filter(
            doctor=request.user
        ).order_by("-appointment_date")

    else:

        appointments = Appointment.objects.all().order_by(
            "-appointment_date"
        )

    return render(
        request,
        "appointment_list.html",
        {"appointments": appointments}
    )


@login_required
@role_required([
    "ADMIN",
    "RECEPTIONIST"
])
def appointment_create(request):

    if request.method == "POST":

        form = AppointmentForm(request.POST)

        if form.is_valid():

            appointment = form.save(commit=False)

            appointment.created_by = request.user

            appointment.save()

            messages.success(
                request,
                "Appointment created successfully."
            )
            return redirect(
            "appointment_detail",
            pk=appointment.pk
        )

    else:

        form = AppointmentForm()

    return render(
        request,
        "appointment_form.html",
        {"form": form}
    )


@login_required
@role_required([
    "ADMIN",
    "RECEPTIONIST",
    "DOCTOR",
    "NURSE"
])
def appointment_detail(request, pk):

    appointment = get_object_or_404(
        Appointment,
        pk=pk
    )

    return render(
        request,
        "appointment_detail.html",
        {"appointment": appointment}
    )


@login_required
@role_required([
    "ADMIN",
    "RECEPTIONIST"
])
def appointment_update(request, pk):

    appointment = get_object_or_404(
        Appointment,
        pk=pk
    )

    if request.method == "POST":

        form = AppointmentForm(
            request.POST,
            instance=appointment
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Appointment updated successfully."
            )

            return redirect(
                "appointment_detail",
                pk=appointment.pk
            )

    else:

        form = AppointmentForm(
            instance=appointment
        )

    return render(
        request,
        "appointment_form.html",
        {
            "form": form,
            "appointment": appointment
        }
    )


@login_required
@role_required([
    "ADMIN"
])
def appointment_delete(request, pk):

    appointment = get_object_or_404(
        Appointment,
        pk=pk
    )

    if request.method == "POST":

        appointment.delete()

        messages.success(
            request,
            "Appointment deleted successfully."
        )

        return redirect(
            "appointment_list"
        )

    return render(
        request,
        "appointment_delete.html",
        {"appointment": appointment}
    )