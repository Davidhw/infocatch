from django.db import models

class Subscription(models.Model):
    url = models.CharField(max_length=100)
    xpath = models.CharField(max_length=100)
# Create your models here.
