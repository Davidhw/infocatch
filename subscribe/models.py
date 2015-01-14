from django.db import models
from django.contrib.auth.models import User

class Subscription(models.Model):
    url = models.CharField(max_length=100)
    xpath = models.CharField(max_length=100)

    def __str__(self):
        return self.url + ": "+self.xpath

    # maybe this should instead be a static method of SubscriptionUserPairing? Maybe it should jush be a top level function of models?
    @staticmethod
    def getStringOfAll(u):
        if u == None:
            return ""
        else:
            pairings = SubscriptionUserPairing.objects.filter(user=u)
            subscriptions = [pair.subscription for pair in pairings]
            return " <br> ".join([str(subscription) for subscription in subscriptions])
#            return " <br> ".join([str(subscription) for subscription in SubscriptionUserPairing.objects.select_related('subscription').filter(user=u)])
#            return " <br> ".join([str(subscription) for subscription in Subscription.objects.filter(subscriptionId in [id for pairing.id for pai SubscriptionUserPairing.objects.filter(userId=uId))])
#        return " <br> ".join([str(subscription) for subscription in Subscription.objects.all()])

class SubscriptionUserPairing(models.Model):
    # too optimistic, too pessimistic :P?
    user = models.ForeignKey(User)
    subscription = models.ForeignKey(Subscription)
            

