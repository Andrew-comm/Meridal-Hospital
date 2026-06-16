# patients/models.py

from django.db import models
from datetime import date
import uuid


class Patient(models.Model):

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]

    STATUS_CHOICES = [
        ("WAITING", "Waiting"),
        ("CONSULTATION", "Consultation"),
        ("LAB", "Laboratory"),
        ("PHARMACY", "Pharmacy"),
        ("COMPLETED", "Completed"),
    ]

    patient_number = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    date_of_birth = models.DateField()

    phone = models.CharField(max_length=20)

    email = models.EmailField(
        blank=True,
        null=True
    )

    address = models.TextField()

    emergency_contact = models.CharField(
        max_length=100,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="WAITING"
    )

    registered_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.patient_number} - {self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):

        # ✅ FIX: ensure unique patient number always
        if not self.patient_number:
            self.patient_number = f"PAT-{uuid.uuid4().hex[:8].upper()}"

        super().save(*args, **kwargs)