from django.shortcuts import render
from django.shortcuts import redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
import json
import urllib2
import sys
import os
from subscribe.models import Subscription
def home(request):
    
    return render_to_response('home-view.html',{"subscriptionsString":Subscription.getStringOfAll()})















