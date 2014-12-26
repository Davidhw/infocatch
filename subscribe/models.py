from django.db import models

class Subscription(models.Model):
    url = models.CharField(max_length=100)
    xpath = models.CharField(max_length=100)

    def __str__(self):
        return self.url + ": "+self.xpath

    @staticmethod
    def getStringOfAll():
        return " <br> ".join([str(subscription) for subscription in Subscription.objects.all()])

            
# Create your models here.
