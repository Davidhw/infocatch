# currently just used for creating an rssfeed for any given user

# based on http://code.runnable.com/Up-BKcQBS3ZKAAG_/how-to-create-rss-feeds-in-django-for-python-and-utils and http://www.lazutkin.com/blog/2005/09/23/code_rss_django/

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from subscribe.models import Subscription,SubscriptionUserPairing,SubscriptionLinks

from django.http import HttpResponse
from django.utils import feedgenerator
import re

import urllib2
from bs4 import BeautifulSoup

from django.contrib.auth.models import User

from getFeeds.downloadFeeds import getSubscriptionLinks
from getFeeds.getPageSource import getPageSource

def RSSFeed(request,userName):
    user = User.objects.get(username=userName)
#    if user = None:
 #       return 

    # create a feed generator having a channel with following title, link and description

    
    feed = feedgenerator.Rss201rev2Feed(
        title=u"%s's RSS Feed" %userName,
        link=u"http://infocatch.herokuapp.com/rss/%s"%userName,
        description=u"A collection of links from %s's subscriptions on Infocatch"%user,
        language=u"en",
    )

    # for each of the user's subscriptions' links, add the link to the feed
    
    for subscriptionUserPairing in SubscriptionUserPairing.objects.filter(user=user):
        try:
            links = SubscriptionLinks.objects.get(subscription = subscriptionUserPairing.subscription).getLinks()
        # the subscription was just created and its links haved been saved yet
        # consider just calling getsubscriptionlinks
        except SubscriptionLinks.DoesNotExist:
            getLinksFromSubscription(subscriptionUserPairing.subscription)
            links = SubscriptionLinks.objects.get(subscription = subscriptionUserPairing.subscription).getLinks()

        for link in links:
            title,description = getTitleAndDescription(link)
#            title,description = "title","description"
            feed.add_item(title=title,link=link,description=description)

    response =  HttpResponse(content_type='application/rss+xml')
    feed.write(response,'utf-8')
    return response


def getTitleAndDescription(link):
    title = "Untitled Article"
    desc = "Undescribed Article"
    html = getPageSource(link,timeout=2)
    if html ==None:
        return title,desc
    else:
        soup = BeautifulSoup(html)
        titleHtml =  soup.title
        descHtml = soup.h1
#        page.close()

        if titleHtml:
            title = titleHtml.getText()

        if descHtml:
            desc = descHtml.getText()

        return title,desc


#    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
#    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 5.1; rv:10.0.1) Gecko/20100101 Firefox/10.0.1')]

#    try:
#        page = opener.open(link,timeout=2)
#    except UrlError:
        # if the page doesn't open, or takes too long to open, just give default title and description
#        return title,desc

    



