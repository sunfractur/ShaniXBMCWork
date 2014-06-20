# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin
import urllib2,urllib,cgi, re
import HTMLParser
import xbmcaddon
import json
import traceback
import os
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP
import time
import sys
import  CustomPlayer

__addon__       = xbmcaddon.Addon()
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')
addon_id = 'plugin.video.shahidmbcnet'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonPath = xbmcaddon.Addon().getAddonInfo("path")
addonArt = os.path.join(addonPath,'resources/images')
#communityStreamPath = os.path.join(addonPath,'resources/community')
communityStreamPath = os.path.join(addonPath,'resources')
communityStreamPath =os.path.join(communityStreamPath,'community')


def PlayStream(sourceEtree, urlSoup, name, url):
    try:
        #url = urlSoup.url.text
        pDialog = xbmcgui.DialogProgress()
        pDialog.create('XBMC', 'Parsing the xml file')
        pDialog.update(10, 'fetching channel info')
        title=''
        link=''
        sc=''
        try:
            title=urlSoup.item.title.text
            
            link=urlSoup.item.link.text
            sc=sourceEtree.findtext('sname')
        except: pass
        if link=='':
            timeD = 2000  #in miliseconds
            line1="couldn't read title and link"
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, timeD, __icon__))
            return False
        regexs = urlSoup.find('regex')
        pDialog.update(80, 'Parsing info')
        if (not regexs==None) and len(regexs)>0:
            liveLink=    getRegexParsed(urlSoup,link)
        else:
            liveLink=    link
        liveLink=liveLink
        if len(liveLink)==0:
            timeD = 2000  #in miliseconds
            line1="couldn't read title and link"
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, timeD, __icon__))
            return False
            
        timeD = 2000  #in miliseconds
        line1="Resource found,playing now."
        pDialog.update(80, line1)
        liveLink=replaceSettingsVariables(liveLink)
        name+='-'+sc+':'+title
        print 'liveLink',liveLink
        pDialog.close()
        listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ), path=liveLink )
        if not 'plugin.video.f4mTester' in liveLink:
            player = CustomPlayer.MyXBMCPlayer()
            start = time.time() 
            #xbmc.Player().play( liveLink,listitem)
            player.play( liveLink,listitem)
            xbmc.sleep(2000)
            while player.is_active:
                xbmc.sleep(200)
            #return player.urlplayed
            done = time.time()
            elapsed = done - start
            if player.urlplayed and elapsed>=3:
                return True
            else:
                return False
        else:
            xbmc.executebuiltin('XBMC.RunPlugin('+liveLink+')')
            return True
                
    except:
        traceback.print_exc(file=sys.stdout)    
    return False  

def getRegexParsed(regexs, url,cookieJar=None,forCookieJarOnly=False,recursiveCall=False,cachedPages={}, rawPost=False):#0,1,2 = URL, regexOnly, CookieJarOnly

#    cachedPages = {}
    #print 'url',url
    doRegexs = re.compile('\$doregex\[([^\]]*)\]').findall(url)
    print 'doRegexs',doRegexs,regexs

    for rege in doRegexs:
        k=regexs.find("regex",{"name":rege})
        if not k==None:
            cookieJarParam=False
            if k.cookiejar:
                cookieJarParam=k.cookiejar.text;
                if  '$doregex' in cookieJarParam:
                    cookieJar=getRegexParsed(regexs, cookieJarParam,cookieJar,True, True,cachedPages)
                    cookieJarParam=True
                else:
                    cookieJarParam=True
            if cookieJarParam:
                if cookieJar==None:
                    #print 'create cookie jar'
                    import cookielib
                    cookieJar = cookielib.LWPCookieJar()
                    #print 'cookieJar new',cookieJar
            page=''
            try:
                page = k.page.text
            except: pass
            if  '$doregex' in page:
                page=getRegexParsed(regexs, page,cookieJar,recursiveCall=True,cachedPages=cachedPages)
                
            postInput=None
            if k.post:
                postInput = k.post.text
                if  '$doregex' in postInput:
                    postInput=getRegexParsed(regexs, postInput,cookieJar,recursiveCall=True,cachedPages=cachedPages)
                print 'post is now',postInput
            
            if k.rawpost:
                postInput = k.rawpost.text
                if  '$doregex' in postInput:
                    postInput=getRegexParsed(regexs, postInput,cookieJar,recursiveCall=True,cachedPages=cachedPages,rawPost=True)
                print 'rawpost is now',postInput    
            link=''    
            if not page=='' and page in cachedPages and forCookieJarOnly==False :
                link = cachedPages[page]
            else:
                if page.startswith('http'):
                    print 'Ingoring Cache',page
                    req = urllib2.Request(page)
                    
                    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
                    if k.referer:
                        req.add_header('Referer', k.referer.text)
                    if k.agent:
                        req.add_header('User-agent', k.agent.text)

                    if not cookieJar==None:
                        #print 'cookieJarVal',cookieJar
                        cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
                        opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
                        opener = urllib2.install_opener(opener)
                    #print 'after cookie jar'

                    post=None
                    if postInput and not k.rawpost:
                        postData=postInput
                        splitpost=postData.split(',');
                        post={}
                        for p in splitpost:
                            n=p.split(':')[0];
                            v=p.split(':')[1];
                            post[n]=v
                        post = urllib.urlencode(post)
                        
                    if postInput and k.rawpost:
                        post=postInput

                    if post:
                        response = urllib2.urlopen(req,post)
                    else:
                        response = urllib2.urlopen(req)

                    link = response.read()
                    link=javascriptUnEscape(link)

                    response.close()
                    cachedPages[page] = link
                    if forCookieJarOnly:
                        return cookieJar# do nothing
                elif not page.startswith('http'):
                    link=page
            
            expres=k.expres.text
            if  '$doregex' in expres:
                expres=getRegexParsed(regexs, expres,cookieJar,recursiveCall=True,cachedPages=cachedPages)
                        
            print 'link',link
            print expres
            if not expres=='':
                if expres.startswith('$pyFunction:'):
                    val=doEval(expres.split('$pyFunction:')[1],link, cookieJar)
                    url = url.replace("$doregex[" + rege + "]", val)
                else:
                    if not link=='': 
                        reg = re.compile(expres).search(link)
                        val=reg.group(1).strip()

                    else:
                        val=expres
                    if k.rawpost:
                        print 'rawpost'
                        val=urllib.quote_plus(val)
                    if k.htmlunescape:
                            #val=urllib.unquote_plus(val)
                        import HTMLParser
                        val=HTMLParser.HTMLParser().unescape(val)
                        
                    url = url.replace("$doregex[" + rege + "]",val )
                        
            else:
                url = url.replace("$doregex[" + rege + "]", '')
            
            if '$epoctime$' in url:
                url=url.replace('$epoctime$',getEpocTime())
            if '$GUID$' in url:
                import uuid
                url=url.replace('$GUID$',str(uuid.uuid1()).upper())
            if '$get_cookies$' in url:
                url=url.replace('$get_cookies$',getCookiesString(cookieJar))   
            
            if recursiveCall: return url
    print 'final url',url
    return url
def getCookiesString(cookieJar):
    try:
        cookieString=""
        for index, cookie in enumerate(cookieJar):
            cookieString+=cookie.name + "=" + cookie.value +";"
    except: pass
    print 'cookieString',cookieString
    return cookieString
    
def getEpocTime():
    import time
    return str(int(time.time()*1000))
    
def javascriptUnEscape(str):
	js=re.findall('unescape\(\'(.*?)\'',str)
	print 'js',js
	if (not js==None) and len(js)>0:
		for j in js:
			print urllib.unquote(j)
			str=str.replace(j ,urllib.unquote(j))
	return str
    
def doEval(fun_call,page_data=None,Cookie_Jar=None):
    ret_val=''
    #if profile not in sys.path:
    #    sys.path.append(profile)
    
    print fun_call
    try:
        py_file='import '+fun_call.split('.')[0]
        #print py_file
        exec( py_file)
    except: pass
    
    exec ('ret_val='+fun_call)
    #exec('ret_val=1+1')
    return str(ret_val)
    
def replaceSettingsVariables(str):
    retVal=str
    if '$setting' in str:
        matches=re.findall('\$(setting_.*?)\$', str)
        for m in matches:
            setting_val=selfAddon.getSetting( m )
            retVal=retVal.replace('$'+m+'$',setting_val)
    return retVal


def send_web_socket(Cookie_Jar,url_to_call):
    try:
        import urllib2
        import base64
        import uuid
        req = urllib2.Request(url_to_call)

        str_guid=str(uuid.uuid1()).upper()
        str_guid=base64.b64encode(str_guid)
        req.add_header('Connection', 'Upgrade')
        req.add_header('Upgrade', 'websocket')

        req.add_header('Sec-WebSocket-Key', str_guid)
        req.add_header('Origin','http://www.streamafrik.com')
        req.add_header('Pragma','no-cache')
        req.add_header('Cache-Control','no-cache')
        req.add_header('Sec-WebSocket-Version', '13')
        req.add_header('Sec-WebSocket-Extensions', 'permessage-deflate; client_max_window_bits, x-webkit-deflate-frame')
        req.add_header('User-Agent','Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.53')
        cookie_handler = urllib2.HTTPCookieProcessor(Cookie_Jar)
        opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
        opener = urllib2.install_opener(opener)
        from keepalive import HTTPHandler
        keepalive_handler = HTTPHandler()
        opener = urllib2.build_opener(keepalive_handler)
        urllib2.install_opener(opener)
        urllib2.urlopen(req)
        response.close()
        return ''
    except: traceback.print_exc(file=sys.stdout)
    return ''

    
def get_unpacked( page_value, regex_for_text, iterations=1, total_iteration=1):
    try:        
        if page_value.startswith("http"):
            page_value= getUrl(page_value)
        print 'page_value',page_value
        if regex_for_text and len(regex_for_text)>0:
            page_value=re.compile(regex_for_text).findall(page_value)[0] #get the js variable

        page_value=unpack(page_value,iterations,total_iteration)
    except: traceback.print_exc(file=sys.stdout)
    print 'unpacked',page_value
    return page_value

def unpack(sJavascript,iteration=1, totaliterations=2  ):
    print 'iteration',iteration
    if sJavascript.startswith('var _0xcb8a='):
        aSplit=sJavascript.split('var _0xcb8a=')
        ss="myarray="+aSplit[1].split("eval(")[0]
        exec(ss)
        a1=62
        c1=int(aSplit[1].split(",62,")[1].split(',')[0])
        p1=myarray[0]
        k1=myarray[3]
        with open('temp file'+str(iteration)+'.js', "wb") as filewriter:
            filewriter.write(str(k1))
        #aa=1/0
    else:

        aSplit = sJavascript.split("rn p}('")
        print aSplit
        
        p1,a1,c1,k1=('','0','0','')
     
        ss="p1,a1,c1,k1=('"+aSplit[1].split(".spli")[0]+')' 
        exec(ss)
    k1=k1.split('|')
    aSplit = aSplit[1].split("))'")
#    print ' p array is ',len(aSplit)
#   print len(aSplit )

    #p=str(aSplit[0]+'))')#.replace("\\","")#.replace('\\\\','\\')

    #print aSplit[1]
    #aSplit = aSplit[1].split(",")
    #print aSplit[0] 
    #a = int(aSplit[1])
    #c = int(aSplit[2])
    #k = aSplit[3].split(".")[0].replace("'", '').split('|')
    #a=int(a)
    #c=int(c)
    
    #p=p.replace('\\', '')
#    print 'p val is ',p[0:100],'............',p[-100:],len(p)
#    print 'p1 val is ',p1[0:100],'............',p1[-100:],len(p1)
    
    #print a,a1
    #print c,a1
    #print 'k val is ',k[-10:],len(k)
#    print 'k1 val is ',k1[-10:],len(k1)
    e = ''
    d = ''#32823

    #sUnpacked = str(__unpack(p, a, c, k, e, d))
    sUnpacked1 = str(__unpack(p1, a1, c1, k1, e, d,iteration))
    
    #print sUnpacked[:200]+'....'+sUnpacked[-100:], len(sUnpacked)
#    print sUnpacked1[:200]+'....'+sUnpacked1[-100:], len(sUnpacked1)
    
    #exec('sUnpacked1="'+sUnpacked1+'"')
    if iteration>=totaliterations:
#        print 'final res',sUnpacked1[:200]+'....'+sUnpacked1[-100:], len(sUnpacked1)
        return sUnpacked1#.replace('\\\\', '\\')
    else:
#        print 'final res for this iteration is',iteration
        return unpack(sUnpacked1,iteration+1)#.replace('\\', ''),iteration)#.replace('\\', '');#unpack(sUnpacked.replace('\\', ''))

def __unpack(p, a, c, k, e, d, iteration):

    #with open('before file'+str(iteration)+'.js', "wb") as filewriter:
    #    filewriter.write(str(p))
    while (c > 1):
        c = c -1
        if (k[c]):
            aa=str(__itoaNew(c, a))
            #re.sub('\\b' + aa +'\\b', k[c], p) THIS IS Bloody slow!
            p=findAndReplaceWord(p,aa,k[c])

            
    #with open('after file'+str(iteration)+'.js', "wb") as filewriter:
    #    filewriter.write(str(p))
    return p

#
#function equalavent to re.sub('\\b' + aa +'\\b', k[c], p)
def findAndReplaceWord(source_str, word_to_find,replace_with):
    splits=None
    splits=source_str.split(word_to_find)
    if len(splits)>1:
        new_string=[]
        current_index=0
        for current_split in splits:
            #print 'here',i
            new_string.append(current_split)
            val=word_to_find#by default assume it was wrong to split

            #if its first one and item is blank then check next item is valid or not
            if current_index==len(splits)-1:
                val='' # last one nothing to append normally
            else:
                if len(current_split)==0: #if blank check next one with current split value
                    if ( len(splits[current_index+1])==0 and word_to_find[0].lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890_') or (len(splits[current_index+1])>0  and splits[current_index+1][0].lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890_'):# first just just check next
                        val=replace_with
                #not blank, then check current endvalue and next first value
                else:
                    if (splits[current_index][-1].lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890_') and (( len(splits[current_index+1])==0 and word_to_find[0].lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890_') or (len(splits[current_index+1])>0  and splits[current_index+1][0].lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890_')):# first just just check next
                        val=replace_with
                        
            new_string.append(val)
            current_index+=1
        #aaaa=1/0
        source_str=''.join(new_string)
    return source_str        

def __itoa(num, radix):
#    print 'num red',num, radix
    result = ""
    if num==0: return '0'
    while num > 0:
        result = "0123456789abcdefghijklmnopqrstuvwxyz"[num % radix] + result
        num /= radix
    return result
	
def __itoaNew(cc, a):
    aa="" if cc < a else __itoaNew(int(cc / a),a) 
    cc = (cc % a)
    bb=chr(cc + 29) if cc> 35 else str(__itoa(cc,36))
    return aa+bb


def getCookiesString(cookieJar):
    try:
        cookieString=""
        for index, cookie in enumerate(cookieJar):
            cookieString+=cookie.name + "=" + cookie.value +";"
    except: pass
    print 'cookieString',cookieString
    return cookieString

def getUrl(url, cookieJar=None,post=None, timeout=20, headers=None):


    cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
    opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    #opener = urllib2.install_opener(opener)
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    if headers:
        for h,hv in headers:
            req.add_header(h,hv)

    response = opener.open(req,post,timeout=timeout)
    link=response.read()
    response.close()
    return link;
