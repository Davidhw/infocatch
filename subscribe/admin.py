from django.contrib import admin
from rssplus.Subscribe.models import Subscription, SubscriptionUserPairing
# Register your models here.
admin.site.register(Subscription)
admin.site.register(SubscriptionUserPairing)
