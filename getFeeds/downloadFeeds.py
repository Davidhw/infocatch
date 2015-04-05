from userSettings.models import UserSettings
import urllib2
from subscribe.models import Subscription,SubscriptionUserPairing
import time
from lxml import etree,html
import pdfkit
from django.core.mail.message import EmailMessage
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import selenium
from rssplus.settings import BASE_DIR



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
#    links = [link for link in linkList for linkList in [getLinksFromSubscription(sub) for sub in subscriptions]]
    # flatten list of lists of links
    links = sum([getLinksFromSubscription(sub) for sub in subscriptions],[])
    config = pdfkit.configuration(wkhtmltopdf= "/app/bin/wkhtmltopdf")
    outputPdf = pdfkit.from_url([str(link) for link in links],False,configuration=config)
    return outputPdf
    

def getEveryUsersFeeds():        
    from selenium import webdriver
#    driver = webdriver.Firefox()
    path_to_ffdriver = BASE_DIR+'chromedriver
    browser = webdriver.Chrome(executable_path = path_to_ffdriver)
    for u in User.objects.all():
        try:
            subscriptions = [sup.subscription for sup in SubscriptionUserPairing.objects.filter(user = u)]
            settings = UserSettings.objects.get(user = u)
        except ObjectDoesNotExist:
            continue
        format = settings.feed_Format
        if format =='p':
            attatchment = getPDFOfFeeds(subscriptions)
            extension = "pdf"
            
        elif format =='e':
            pass
        elif format == 't':
            pass

        emailFeed(settings.email,attatchment,extension)


def getLinksFromSubscription(sub):
    '''
    try:
        response = urllib2.urlopen(sub.url)
    except:
        return []
    htmlparser = etree.HTMLParser()
    tree = etree.parse(response, htmlparser)
    elements = tree.xpath(sub.xpath)
    return [element.values()[1] for element in elements]
    '''
    driver.get(sub.url)
    elements = driver.find_elements_by_xpath(sub.xpath)
    return [element.get_attribute('href') for element in elements]
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
