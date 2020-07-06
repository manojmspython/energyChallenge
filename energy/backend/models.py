from django.db import models


class NemData(models.Model):
    """
    This model save the row details of Nem 13 file for indicator 250.
    """
    nmi = models.CharField(max_length=128, blank=True, null=True)
    serialNumber = models.CharField(max_length=128, blank=True, null=True)
    reading = models.CharField(max_length=128, blank=True, null=True)
    dateTime = models.CharField(max_length=128, blank=True, null=True)
    flowName = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return f"Reading: {self.reading},   DateTime: {self.dateTime}"
