from django.db import models


class NemData(models.Model):
    """
    This model save the row details of Nem 13 file for indicator 250.
    """
    nmi = models.CharField(max_length=128)
    serialNumber = models.CharField(max_length=128)
    reading = models.CharField(max_length=128)
    dateTime = models.CharField(max_length=128)
    flowName = models.CharField(max_length=128)

    def __str__(self):
        return f"Reading: {self.reading},   DateTime: {self.dateTime}"
