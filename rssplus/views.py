from django.shortcuts import render,redirect, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from forms import URLForm
from django.contrib.auth import logout as auth_logout


import json
import urllib2
import sys
import os
from subscribe.models import Subscription
from subscribe.views import DeleteUserSubPairView

#https://github.com/omab/python-social-auth/blob/master/examples/django_example/example/app/views.py
def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')

def home(request):
    form = URLForm()
    if request.user and not request.user.is_anonymous():
        user = request.user
    else:
        user = None
    return render(request,'home-view.html',{"subscriptionsString":Subscription.getStringOfAll(user),"urlForm":form})
#    return render_to_response('home-view.html',{"subscriptionsString":Subscription.getStringOfAll(),"urlForm":form})















