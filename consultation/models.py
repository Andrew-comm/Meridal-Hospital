from django.db import models

from patients.models import Patient
from Accounts.models import User


class Consultation(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    symptoms = models.TextField()

    diagnosis = models.TextField()

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )