from django.db import models

from patients.models import Patient
from Accounts.models import User


class Appointment(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "DOCTOR"}
    )

    appointment_date = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        default="Scheduled"
    )

    reason = models.TextField()

    def __str__(self):
        return f"{self.patient}"