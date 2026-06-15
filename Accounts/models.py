from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ADMIN = "ADMIN"
    DOCTOR = "DOCTOR"
    NURSE = "NURSE"
    RECEPTIONIST = "RECEPTIONIST"
    PHARMACIST = "PHARMACIST"
    LAB_TECH = "LAB_TECH"

    ROLE_CHOICES = [
        (ADMIN, "Admin"),
        (DOCTOR, "Doctor"),
        (NURSE, "Nurse"),
        (RECEPTIONIST, "Receptionist"),
        (PHARMACIST, "Pharmacist"),
        (LAB_TECH, "Lab Technician"),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )