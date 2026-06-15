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


# patients/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import PatientForm
from .models import Patient

from Accounts.decorators import role_required


@login_required
@role_required(["ADMIN", "RECEPTIONIST"])
def patient_create(request):

    if request.method == "POST":

        form = PatientForm(request.POST)

        if form.is_valid():

            patient = form.save()

            messages.success(
                request,
                f"Patient {patient.patient_number} registered successfully."
            )

            return redirect(
                "patient_detail",
                pk=patient.pk
            )

    else:

        form = PatientForm()

    return render(
        request,
        "patients/patient_form.html",
        {"form": form}
    )

@login_required
def patient_detail(request, pk):

    patient = Patient.objects.get(pk=pk)

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