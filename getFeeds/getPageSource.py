import urllib2
import re
from selenium import webdriver
from rssplus.settings import BASE_DIR, BASE_URL

def removeJavascript(pageSource,allJavascript=True):
    # just remove the script tags
#    if allJavascript:
    return re.sub(r'<script.+</script>','',pageSource,flags=re.DOTALL)
#    else:
 #       return re.sub(r'<script.+</script>','',pageSource)
#    from django.utils.html import strip_tags                                  
#    return strip_tags(pageSource)                                             
#    cleaner = Cleaner()                                                       
#    cleaner.javascript = True                                                 
#    cleaner.style = False                                                     
#    print >>sys.stderr, "pritning s"                                          
#    s =  lxml.html.tostring(cleaner.clean_html(lxml.html.fromstring(pageSource)),encoding='unicode')                                                         
#    s = lxml.html.tostring(lxml.html.fromstring(pageSource))                  
#    print >>sys.stderr, s                                                     
#    return s                                                                  
#    from lxml import etree                                                    
#    return lxml.html.tostring(cleaner.clean_html(etree.fromstring(pageSource)),encoding='unicode') 

def getPageSourceWithRunningJavascript(link):
    path_to_driver = BASE_DIR+'/phantomjs-1.9.1-linux-x86_64/bin/phantomjs'  
    browser =webdriver.PhantomJS(executable_path = path_to_driver,service_args = ['--ssl-protocol=TLSv1'])                                                    
    browser.get(link)                                                           
    html = browser.page_source                               
    browser.quit()   
    return html
'''
    if keepJavascript==2:
        return removeJavascript(html)
    elif keepJavascript ==1:
        return removeJavascript(html,allJavascript=False)
    else:
        return html
'''
def getPageSource(link,timeout=None):
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 5.1; rv:10.0.1) Gecko/20100101 Firefox/10.0.1')]

    try:
        if timeout == None:
            page = opener.open(link)
        else:
            page = opener.open(link,timeout=timeout)

        sourceLines = page.readlines()
        page.close()
        opener.close()
        return '\n'.join(sourceLines)

    except:
        return None
