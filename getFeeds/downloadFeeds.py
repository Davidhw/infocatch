
from userSettings.models import UserSettings
import urllib2
from subscribe.models import Subscription,SubscriptionUserPairing,SubscriptionLinks
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
import datetime


#http://stackoverflow.com/questions/11465555/can-we-use-xpath-with-beautifulsoup

def ensureAbsolute(scrapedUrl,scrapedFromUrl):
    if scrapedUrl[0]=='/':
        if scrapedFromUrl[-1]=='/':
            return scrapedFromUrl+scrapedUrl[1:]
        else:
            return scrapedFromUrl+scrapedUrl
    else:
        return scrapedUrln

def getPDFOfLinks(links):
#    links = [link for link in linkList for linkList in [getLinksFromSubscription(sub) for sub in subscriptions]]
    # flatten list of lists of links
    print links
    '''
    i = 1
    FILENAME = 'tempHtmlFile'
    fileNameStrings = []
    import os
    currentPath = os.getcwd()
    for link in links:
        try:
            response = urllib2.urlopen(link)
            page_content = response.read()
            fname = currentPath+'/'+'getFeeds/'+FILENAME+str(i)+".html"
            with open(fname, 'w') as temp:
                temp.write(page_content)
            fileNameStrings.append(fname)
            i = i+1
        except:
            pass
    
#    fileNameStrings = [FILENAME+str(ii+1) for ii in range(i)]
    '''
    options = {
    'load-error-handling': 'skip',
    'load-media-error-handling': 'skip',
    'disable-javascript':None
    }


    toc = {
    'toc-header-text':"Table Of Contents!"
    }

    config = pdfkit.configuration(wkhtmltopdf= "/app/bin/wkhtmltopdf")

#    outputpdf = pdfkit.from_file(fileNameStrings,"out.pdf",configuration = config)
#    outputPdf = pdfkit.from_file(fileNameStrings,False,configuration = config)

    

    outputPdf = pdfkit.from_url(links,False,configuration=config,toc=toc,options=options)

    return outputPdf
    

def getSubscriptionLinks(u,browser):
    links = []
    for subUserPair in SubscriptionUserPairing.objects.filter(user = u):
        try:
            for link in getLinksFromSubscription(subUserPair.subscription,browser):
                links.append(str(link))
        except ObjectDoesNotExist:
            pass
    return links

    

def getEveryUsersFeeds():        
#    from selenium import webdriver
#    driver = webdriver.Firefox()
    path_to_driver = BASE_DIR+'/phantomjs-1.9.1-linux-x86_64/bin/phantomjs'
    browser = webdriver.PhantomJS(executable_path = path_to_driver,service_args=['--ssl-protocol=TLSv1'])
#    browser = webdriver.PhantomJS()
    for u in User.objects.all():
        links = getSubscriptionLinks(u,browser)
        if len(links) == 0:
            print "No links for this user."
            pass
        else:
            settings = UserSettings.objects.get_or_create(user = u,defaults={'email_Feeds_To': u.email,'feed_Format':UserSettings.PDF})[0]
            format = settings.feed_Format
            if format ==UserSettings.PDF:
                linkGroupSize = 10
                if len(links)> linkGroupSize:
                    linkGroups = [links[i*linkGroupSize:(i+1)*linkGroupSize] for i in range(len(links)/linkGroupSize)]
                    for linkGroup in linkGroups:
                        emailFeed(settings.email_Feeds_To,attachment=getPDFOfLinks(linkGroup),extension="pdf")
                else:
                    emailFeed(settings.email_Feeds_To,attachment=getPDFOfLinks(links),extension="pdf")
    #            attachment = getPDFOfLinks(links)
    #            extension = "pdf"
                
            elif format =='e':
                pass
            elif format == UserSettings.EMAIL_LINKS_BATCH:
                # email the links all at once, space delimited
                emailFeed(settings.email_Feeds_To,message=reduce(lambda x,y: x+ ' '+y, links))
            elif format == UserSettings.EMAIL_LINKS_INDIVIDUALLY:
                # email the links one at a time
                for link in links:
                    emailFeed(settings.email_Feeds_To,message=link)
    

#        emailFeed(settings.email,attachment,extension)


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
    subscriptionLinks = SubscriptionLinks.objects.get_or_create(subscription = sub)[0]
    todaysDate = datetime.date.today() 
    # if we've already determined todays links, just return them
    if subscriptionLinks.date == todaysDate:
        return subscriptionLinks.getLinks()

    # otherwise, save the links currently on the page and return the new ones
    else:
        browser.get(sub.url)
        elements = browser.find_elements_by_xpath(sub.xpath)
        linksOnPage = [element.get_attribute('href') for element in elements]

        # determine which links are new
        newLinks = [link for link in linksOnPage if link not in subscriptionLinks.getLinks()]

        #update which links are stored
        subscriptionLinks.update(todaysDate,linksOnPage)

        return newLinks

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
def emailFeed(send_to,message=None,attachment=None,extension=None):
    email = EmailMessage()
    email.subject = "InfoCatch Feed"

    email.from_email = "davidhweinstein@gmail.com"
    email.to = [ send_to, ] 

    if extension == None:
        mType = "text/plain"
        email.body = message
    elif extension=="pdf":
        email.body = "Please find your feed attatched."
        mType = "application/pdf"
        email.attach(filename = "newspaper", mimetype = mType, content = attachment)
    email.send()
