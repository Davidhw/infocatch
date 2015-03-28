from django.contrib import admin
from subscribe.models import Subscription, SubscriptionUserPairing
# Register your models here.
admin.site.register(Subscription)
admin.site.register(SubscriptionUserPairing)
