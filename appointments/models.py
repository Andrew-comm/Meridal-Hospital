from django.db import models

from patients.models import Patient
from Accounts.models import User


class Appointment(models.Model):

    STATUS_CHOICES = [
        ("WAITING", "Waiting"),
        ("CONSULTATION", "Consultation"),
        ("LAB", "Laboratory"),
        ("PHARMACY", "Pharmacy"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    doctor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"role": "DOCTOR"},
        related_name="doctor_appointments"
    )

    appointment_date = models.DateTimeField()

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="WAITING"
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_appointments"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-appointment_date"]

    def __str__(self):

        doctor_name = (
            self.doctor.get_full_name()
            if self.doctor
            else "Unassigned"
        )

        return (
            f"{self.patient.patient_number} - "
            f"{self.patient.first_name} "
            f"{self.patient.last_name} "
            f"({doctor_name})"
        )