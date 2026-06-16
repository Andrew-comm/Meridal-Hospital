from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.db.models import Q

from .models import Patient
from .forms import PatientForm

from Accounts.decorators import role_required


@login_required
@role_required([
    "ADMIN",
    "RECEPTIONIST",
    "DOCTOR",
    "NURSE"
])
def patient_list(request):

    query = request.GET.get("q")

    patients = Patient.objects.all()

    if query:
        patients = patients.filter(
            Q(patient_number__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(phone__icontains=query)
        )

    return render(
        request,
        "patient_list.html",
        {"patients": patients}
    )


@login_required
@role_required([
    "ADMIN",
    "RECEPTIONIST"
])
def patient_create(request):

    if request.method == "POST":

        form = PatientForm(request.POST)

        if form.is_valid():

            patient = form.save(commit=False)

            patient.registered_by = request.user

            patient.save()

            messages.success(
                request,
                f"Patient {patient.patient_number} created successfully."
            )

            return redirect("patient_detail", pk=patient.pk)

    else:
        form = PatientForm()

    return render(
        request,
        "patient_form.html",
        {"form": form}
    )



@login_required
@role_required([
    "ADMIN",
    "RECEPTIONIST",
    "DOCTOR",
    "NURSE",
    "LAB_TECH",
    "PHARMACIST"
])



def patient_detail(request, pk):

    patient = get_object_or_404(Patient, pk=pk)

    return render(
        request,
        "patient_detail.html",
        {"patient": patient}
    )



@login_required
@role_required([
    "ADMIN",
    "RECEPTIONIST"
])
def patient_update(request, pk):

    patient = get_object_or_404(Patient, pk=pk)

    if request.method == "POST":

        form = PatientForm(request.POST, instance=patient)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Patient updated successfully."
            )

            return redirect("patient_detail", pk=patient.pk)

    else:
        form = PatientForm(instance=patient)

    return render(
        request,
        "patient_form.html",
        {"form": form, "patient": patient}
    )





@login_required
@role_required([
    "ADMIN"
])
def patient_delete(request, pk):

    patient = get_object_or_404(Patient, pk=pk)

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