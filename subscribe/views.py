from django.shortcuts import render, render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import json
import sys
import os
from models import Subscription,SubscriptionUserPairing
#from rssplus.views import home
from rssplus.settings import BASE_URL
import time
import re
from getFeeds.getPageSource import getPageSourceWithRunningJavascript,removeJavascript
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse_lazy


class DeleteUserSubPairView(ListView):
    model = SubscriptionUserPairing
#    success_url = reverse_lazy('home')

    def get_object(self):
        try:
            return SubscriptionUserPairing.objects.filter(user=self.request['user'])
        except:
            return None
    

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
def save(request):
    body = json.loads(request.body)

    if request.user and not request.user.is_anonymous():
        if body['url'][-1]=="/":
            body['url'] = body['url'][:-2]

        # if the feed doesn't exst yet, make it
        subscription,subscriptionCreated = Subscription.objects.get_or_create(url = body['url'],xpath=body['xpath'])
        if subscriptionCreated:
            subscription.save()

        # if the current user hasn't subscribed to that feed yet, subscribe them
        subscriptionUserPairing,pairingCreated = SubscriptionUserPairing.objects.get_or_create(user = request.user,subscription=subscription)
        if pairingCreated:
            subscriptionUserPairing.save()

    return redirect('home')


def load_external_page_site_not_specified_in_URL(request):
    from rssplus.forms import URLForm
    try:
        url = URLForm(request.POST).data["siteUrl"]
        return load_external_page(request,url)
    except:
        return redirect('home')
    

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
#    html = urllib2.urlopen(url).read()
    '''
    path_to_driver = BASE_DIR+'/phantomjs-1.9.1-linux-x86_64/bin/phantomjs'
    browser = webdriver.PhantomJS(executable_path = path_to_driver,service_args=['--ssl-protocol=TLSv1'])
    browser.get(url)
    html = removeJavascript(browser.page_source)
    browser.quit()
    '''
    html = getPageSourceWithRunningJavascript(url)
    # </head> was sometimes getting removed with javascript (?!) so just removing it after split
    split = html.split("</head>")
    if len(split)==2:
        html1 = split[0]+"</head>"
        html2 = split[1]
    else:
        html1 = html
        html2 = ""

    # make the base url infocatch so that any site that sets the base url can still load the clickBehavior script from a relative link
    # we don't worry about html2, because the base has to be set in the header tag
    html1 = re.sub(r'<base href.*>','<base href = "'+BASE_URL+'">',html1)

    return render(request,'subscribe-view.html',{'html1':html1,'html2':html2,'url':url})




'''
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(pageSource.lower())
    for element in soup.findAll('script'):
        element.extract()
    return force_text(soup.getText,
'''











