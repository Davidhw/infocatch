from django.shortcuts import render, render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import json
import urllib2
import sys
import os
from models import Subscription
from rssplus.views import home

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# Create your views here.
'''
def console_debug(f):
    def x(*args, **kw):
        try:
            ret = f(*args, **kw)
        except Exception, e:
            print >> sys.stderr, "ERROR:", str(e)
            exc_type, exc_value, tb = sys.exc_info()
            message = "Type: %s\nValue: %s\nTraceback:\n\n%s" % (exc_type, exc_value, "\n".join(traceback.format_tb(tb)))
            print >> sys.stderr, message
            raise
        else:
            return ret
        return x
'''
def save(request):
#    body = simplejson.loads(request.body)
    body = json.loads(request.body)

    with open("RSSlog.txt",'w')as log:
        log.write(str(body.items()))
        log.write("in save")

    url = body['url']
    xpath = body['xpath']
    subscription = Subscription()
    subscription.url = url
    subscription.xpath = xpath
    subscription.save()
#    return load_external_page(request,url)
#    return redirect("http://127.0.0.1:8000/", permanent=True)
#    return HttpResponseRedirect(reverse('rssplus:home'))
#    return HttpResponseRedirect("127.0.0.1:8000")
    from rssplus.forms import URLForm
    form = URLForm()
    return render('home-view.html',{"subscriptionsString":Subscription.getStringOfAll(),"urlForm":form})


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















