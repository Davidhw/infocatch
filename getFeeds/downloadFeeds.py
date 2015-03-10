from userSettings.models import UserSettings
import urllib2
from subscribe.models import Subscription
import time
from lxml import etree,html
import pdfkit
from django.core.mail.message import EmailMessage

#http://stackoverflow.com/questions/11465555/can-we-use-xpath-with-beautifulsoup

def ensureAbsolute(scrapedUrl,scrapedFromUrl):
    if scrapedUrl[0]=='/':
        if scrapedFromUrl[-1]=='/':
            return scrapedFromUrl+scrapedUrl[1:]
        else:
            return scrapedFromUrl+scrapedUrl
    else:
        return scrapedUrl

def getPDFOfFeeds(subscriptions):
    links = [link for link in linkList for linkList in [getLinksFromSubscription(sub) for sub in subscriptions]]
    outputPdf = pdfkit.from_url([str(link) for link in links],False)
    return outputPdf
    

def getEveryUsersFeeds():        
    for u in User.objecs.all():
        subscriptions = [sup.subscription for sup in SubscriptionUserPairing.objects.filter(user = u)]
        settings = UserSettings.objects.get(user = u)
        format = settings.format
        if format =='p':
            attatchment = getPDFOfFeeds(subscriptions)
            extension = "pdf"
            
        elif format =='e':
            pass
        elif format == 't':
            pass

        emailFeed(settings.email,attatchment,extension):


def getLinksFromSubscription(sub):
    response = urllib2.urlopen(sub.url)
    htmlparser = etree.HTMLParser()
    tree = etree.parse(response, htmlparser)
    elements = tree.xpath(sub.xpath)
    return [element.values()[1] for element in elements]
'''    
    for elmement in elements:
        htmls = [html.fromstring(urllib2.urlopen(ensureAbsolute(element.values()[1],sub.url)).read()) for element in elements]
''' 

#http://twigstechtips.blogspot.com/2012/01/django-send-email-with-attachment.html
def emailFeed(send_to,attatchment,extension):
    if extension=="pdf":
        mType = "application/pdf"

    email = EmailMessage()
    email.subject = "InfoCatch Feed"
    email.body = "Please find your feed attatched."
    email.from_email = "davidhweinstein@gmail.com"
    email.to = [ send_to, ] 
    email.attach(filename = "newspaper", mimetype = mType, content = attatchment)
    email.send()
