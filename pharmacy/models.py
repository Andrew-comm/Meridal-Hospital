from django.db import models

# Create your models here.
class Medicine(models.Model):

    name = models.CharField(max_length=100)

    stock = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

from consultation.models import Consultation


class Prescription(models.Model):

    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.CASCADE
    )

    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE
    )

    dosage = models.CharField(
        max_length=100
    )

    quantity = models.PositiveIntegerField()    