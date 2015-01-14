from django.shortcuts import render, render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import json
import urllib2
import sys
import os
from models import Subscription,SubscriptionUserPairing
from rssplus.views import home

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
def save(request):
    body = json.loads(request.body)

    if request.user and not request.user.is_anonymous():
        with open("RSSlog.txt",'w')as log:
            log.write(str(body.items()))
            log.write("in save")

        # if the feed doesn't exst yet, make it
        subscription,subscriptionCreated = Subscription.objects.get_or_create(url = body['url'],xpath=body['xpath'])
        if subscriptionCreated:
            subscription.save()

        # if the current user hasn't subscribed to that feed yet, subscribe them
        subscriptionUserPairing,pairingCreated = SubscriptionUserPairing.objects.get_or_create(user = request.user,subscription=subscription)
        if pairingCreated:
            subscriptionUserPairing.save()

#    return load_external_page(request,url)
#    return redirect("http://127.0.0.1:8000/", permanent=True)
#    return HttpResponseRedirect(reverse('rssplus:home'))
#    return HttpResponseRedirect("127.0.0.1:8000")
    from rssplus.forms import URLForm
    form = URLForm()
#    return render('home-view.html',{"subscriptionsString":Subscription.getStringOfAll(),"urlForm":form})
#    return render('home-view.html',{"subscriptionsString":Subscription.getStringOfAll(),"urlForm":None})
    return redirect('home')


def load_external_page_site_not_specified_in_URL(request):
    from rssplus.forms import URLForm
    url = URLForm(request.POST).data["siteUrl"]
    return load_external_page(request,url)

def load_external_page(request,url):

    def addHttp(url):
        http = "http://"
        if url[:7]==http:
                pass
        elif url[:8] == "https://":
                url = http+url[8:]
        else:
                url = http+url
        return url
    
    url = addHttp(url)
    html = urllib2.urlopen(url).read()
    split = html.split("</head>")
    if len(split)==2:
        html1 = html[0:len(split[0])+len("</head>")]
        html2 = split[1]
    else:
        html1 = html
        html2 = ""
#    html1 = html.split("/head>")[0]
#    html2 = html.split("/head>")[1]
#    html = "<h1 hi />"
#    return render(request,'subscribe-view.html')
#    return render(request,'subscribe-view.html',{'html':html,'url':url},dirs = (PROJECT_ROOT+"/subscribe/templates/subscribe/",PROJECT_ROOT+"subscribe/templates/"))
#    with open("RSSlog.txt",'w') as log:
#        log.write("writing html of"+url)
#        log.write(url)
    return render(request,'subscribe-view.html',{'html1':html1+"Click on the content you want. The service will highlight what it thinks you want. Deselect the content you do not want or make the selection criteria more general by hitting the up arrow on your keyboard. Subscribe to the highlighted content by hitting the right arrow.",'html2':html2,'url':url})















