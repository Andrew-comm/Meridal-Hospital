# patients/models.py

from django.db import models
from datetime import date


class Patient(models.Model):

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
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

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.patient_number} - {self.first_name} {self.last_name}"

    @property
    def age(self):
        today = date.today()

        return (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (
                    self.date_of_birth.month,
                    self.date_of_birth.day
                )
            )
        )

    def save(self, *args, **kwargs):

        if not self.patient_number:

            last_patient = Patient.objects.order_by(
                "-id"
            ).first()

            if last_patient:
                last_id = last_patient.id + 1
            else:
                last_id = 1

            self.patient_number = f"PAT-{last_id:05d}"

        super().save(*args, **kwargs)