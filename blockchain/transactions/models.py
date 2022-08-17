from django.db import models


class Transaction(models.Model):
    transaction_pk = models.CharField(max_length=64)
    description = models.TextField()
    value = models.DecimalField(max_digits=16, decimal_places=8)
    datetime = models.DateTimeField(auto_now=True)
    jsontext = models.TextField()
