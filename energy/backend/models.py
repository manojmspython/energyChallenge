from django.db import models

# Create your models here.


class NemData(models.Model):
    """
    This model save the details of citizen in Paranuara.
    """
    nmi = models.CharField(max_length=128, blank=True, null=True)
    serialNumber = models.CharField(max_length=128, blank=True, null=True)
    reading = models.CharField(max_length=128, blank=True, null=True)
    dateTime = models.CharField(max_length=128, blank=True, null=True)
    flowName = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return f"Reading: {self.reading},   DateTime: {self.dateTime}"
