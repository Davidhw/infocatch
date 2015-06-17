from django.shortcuts import render,redirect, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from forms import URLForm
from django.contrib.auth import logout as auth_logout


import json
import urllib2
import sys
import os
from subscribe.models import Subscription,SubscriptionUserPairing
from subscribe.views import DeleteUserSubPairView

#https://github.com/omab/python-social-auth/blob/master/examples/django_example/example/app/views.py
def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')

def home(request):
    form = URLForm()
    subscriptionUserPairList = None
    if request.user and not request.user.is_anonymous():
        user = request.user
        if request.POST:
            delPairs = request.POST.getlist('todelete')
            SubscriptionUserPairing.objects.filter(pk__in = delPairs).delete()

        subscriptionUserPairList = SubscriptionUserPairing.objects.filter(user=user)
    else:
        user = None
    
    return render(request,'home-view.html',{"subscriptionUserPairList":subscriptionUserPairList,"urlForm":form})
#    return render_to_response('home-view.html',{"subscriptionsString":Subscription.getStringOfAll(),"urlForm":form})















