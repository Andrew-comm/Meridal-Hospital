from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Patient
from .forms import PatientForm


@login_required
def patient_list(request):

    patients = Patient.objects.all().order_by("-id")

    return render(
        request,
        "patient_list.html",
        {"patients": patients}
    )


@login_required
def patient_create(request):

    if request.method == "POST":

        form = PatientForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Patient registered successfully."
            )

            return redirect("patient_list")

    else:
        form = PatientForm()

    return render(
        request,
        "patient_form.html",
        {"form": form}
    )


@login_required
def patient_detail(request, pk):

    patient = get_object_or_404(
        Patient,
        pk=pk
    )

    return render(
        request,
        "patients/patient_detail.html",
        {"patient": patient}
    )


@login_required
def patient_update(request, pk):

    patient = get_object_or_404(
        Patient,
        pk=pk
    )

    if request.method == "POST":

        form = PatientForm(
            request.POST,
            instance=patient
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Patient updated successfully."
            )

            return redirect(
                "patient_detail",
                pk=patient.id
            )

    else:
        form = PatientForm(instance=patient)

    return render(
        request,
        "patient_form.html",
        {"form": form}
    )


@login_required
def patient_delete(request, pk):

    patient = get_object_or_404(
        Patient,
        pk=pk
    )

    if request.method == "POST":

        patient.delete()

        messages.success(
            request,
            "Patient deleted successfully."
        )

        return redirect("patient_list")

    return render(
        request,
        "patient_delete.html",
        {"patient": patient}
    )