from django.db import models

from patients.models import Patient


class LabRequest(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    test_name = models.CharField(
        max_length=200
    )

    status = models.CharField(
        max_length=20,
        default="Pending"
    )

    requested_at = models.DateTimeField(
        auto_now_add=True
    )

class LabResult(models.Model):

    lab_request = models.OneToOneField(
        LabRequest,
        on_delete=models.CASCADE
    )

    result = models.TextField()

    completed_at = models.DateTimeField(
        auto_now_add=True
    )
