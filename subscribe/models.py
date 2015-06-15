from django.db import models
from django.contrib.auth.models import User
import datetime
import simplejson

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
            
class SubscriptionLinks(models.Model):
    subscription = models.ForeignKey(Subscription)
    links = models.CharField(max_length=4000)
    # make the date automatically when the object is created. the lack of parens in date.today means that the function gets passed rather than evaluating the date when the model is first defined.
    date = models.DateField(blank=True,null=True)

 # getters and setters for links (so that we can store a list) based on http://stackoverflow.com/questions/22340258/django-list-field-in-model
    def setLinks(self, links):
        self.links = simplejson.dumps(links)

    def getLinks(self):
        if self.links == "":
            return []
        else:
            return simplejson.loads(self.links)

    def update(self,date,links):
        self.date = date
        self.setLinks(links)
        self.save()
