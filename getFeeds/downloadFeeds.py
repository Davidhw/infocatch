
from userSettings.models import UserSettings
import urllib2
from subscribe.models import Subscription,SubscriptionUserPairing
import time
from lxml import etree,html
import pdfkit
from django.core.mail.message import EmailMessage
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from selenium import webdriver
from rssplus.settings import BASE_DIR
#from getFeeds.getHtml import GetHtml
from lxml import html


#http://stackoverflow.com/questions/11465555/can-we-use-xpath-with-beautifulsoup

def ensureAbsolute(scrapedUrl,scrapedFromUrl):
    if scrapedUrl[0]=='/':
        if scrapedFromUrl[-1]=='/':
            return scrapedFromUrl+scrapedUrl[1:]
        else:
            return scrapedFromUrl+scrapedUrl
    else:
        return scrapedUrl

def getPDFOfLinks(links):
#    links = [link for link in linkList for linkList in [getLinksFromSubscription(sub) for sub in subscriptions]]
    # flatten list of lists of links
    config = pdfkit.configuration(wkhtmltopdf= "/app/bin/wkhtmltopdf")
    outputPdf = pdfkit.from_url([str(link) for link in links],False,configuration=config)
    return outputPdf
    

def getSubscriptionLinks(u,browser):
    links = []
    for sub in SubscriptionUserPairing.objects.filter(user = u):
        try:
            links.append(getLinksFromSubscription(sub,browser))
        except ObjectDoesNotExist:
            pass
    return links

    

def getEveryUsersFeeds():        
#    from selenium import webdriver
#    driver = webdriver.Firefox()
    path_to_driver = BASE_DIR+'/phantomjs-1.9.1-linux-x86_64/bin/phantomjs'
    browser = webdriver.PhantomJS(executable_path = path_to_driver)
#    browser = webdriver.PhantomJS()
    for u in User.objects.all():
        links = getSubscriptionLinks(u,browser)
        settings = UserSettings.objects.get(user = u)
        format = settings.feed_Format
        if format =='p':
            attatchment = getPDFOfLinks(links)
            extension = "pdf"
            
        elif format =='e':
            pass
        elif format == 't':
            pass

        emailFeed(settings.email,attatchment,extension)


def getLinksFromSubscription(sub,browser):
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
    browser.get(sub.url)
    elements = browser.find_elements_by_xpath(sub.xpath)
    return [element.get_attribute('href') for element in elements]

    # html is the etree's html parser
    '''
    pageHtml = GetHtml.get_Html(sub.url)
    tree = html.fromstring(pageHtml)
    links = tree.xpath(sub.xpath)
    return [ensureAbsolute(link,sub.url) for link in links]
    '''

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
