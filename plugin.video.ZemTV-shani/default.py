import xbmc, xbmcgui, xbmcplugin
import urllib2,urllib,cgi, re, urlresolver
import urlparse
import HTMLParser
import xbmcaddon
from operator import itemgetter
import traceback
import base64

__addon__       = xbmcaddon.Addon()
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')
addon_id = 'plugin.video.ZemTV-shani'
selfAddon = xbmcaddon.Addon(id=addon_id)
  
 
mainurl='http://www.zemtv.com/'
liveURL='http://www.zemtv.com/live-pakistani-news-channels/'

tabURL ='http://www.eboundservices.com:8888/users/rex/m_live.php?app=%s&stream=%s'

def ShowSettings(Fromurl):
	selfAddon.openSettings()
	
def addLink(name,url,iconimage):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok


def addDir(name,url,mode,iconimage,showContext=False,showLiveContext=False,isItFolder=True, linkType=None):
#	print name
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )

	if showContext==True:
		cmd1 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "DM")
		cmd2 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "LINK")
		cmd3 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "Youtube")
		cmd4 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "PLAYWIRE")
		cmd5 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "EBOUND")
		cmd6 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "PLAYWIRE")
		
		liz.addContextMenuItems([('Show All Sources',cmd6),('Play Ebound video',cmd5),('Play Playwire video',cmd4),('Play Youtube video',cmd3),('Play DailyMotion video',cmd1),('Play Tune.pk video',cmd2)])
	if linkType:
		u="XBMC.RunPlugin(%s&linkType=%s)" % (u, linkType)
		
	if showLiveContext==True:
		cmd1 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "RTMP")
		cmd2 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "HTTP")
		liz.addContextMenuItems([('Play RTMP Steam (flash)',cmd1),('Play Http Stream (ios)',cmd2)])
	
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isItFolder)
	return ok
	
def PlayChannel ( channelName ): 
#	print linkType
	url = tabURL.replace('%s',channelName);
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
#	print link
	
	match=re.compile('\"(http.*?playlist.m3u.*?)\"').findall(link)
#	print match

	strval = match[0]
#	print strval
	req = urllib2.Request(strval)
	req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
	req.add_header('Referer', 'http://www.eboundservices.com:8888/users/rex/m_live.php')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
#	print link
	match=re.compile('\"(http.*?hashAESkey=.*?)\"').findall(link)
#	print match
	strval = match[0]

	listitem = xbmcgui.ListItem(channelName)
	listitem.setInfo('video', {'Title': channelName, 'Genre': 'Live TV'})
	playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
	playlist.clear()
	playlist.add (strval)

	xbmc.Player().play(playlist)
	return


def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
				
	return param


def DisplayChannelNames(url):
	req = urllib2.Request(mainurl)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
#	print link
#	 match=re.compile('<param name="URL" value="(.+?)">').findall(link)
#	match=re.compile('<a href="(.+?)"').findall(link)
#	match=re.compile('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>').findall(link)
#	match =re.findall('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>', link, re.DOTALL|re.IGNORECASE)


	match =re.findall('onclick="playChannel\(\'(.*?)\'\);".?>(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
#	print match
#	print 'val is'
	match=sorted(match,key=itemgetter(1)   )
	for cname in match:
		if cname[0]<>'':
			addDir(cname[1] ,cname[0] ,1,'',isItFolder=False)
	return

def Addtypes():
	addDir('Shows' ,'Shows' ,2,'')
	addDir('Live Channels' ,'Live' ,2,'')
	addDir('Settings' ,'Live' ,6,'',isItFolder=False)
	return

def AddEnteries(type):
#	print "addenT"
	if type=='Shows':
		AddShows(mainurl)
	elif type=='Next Page':
		AddShows(url)
	else:
		#addDir(Colored('ZemTv Channels','ZM',True) ,'ZEMTV' ,10,'', False, True,isItFolder=False)		#name,url,mode,icon
		#AddChannels();#AddChannels()
		addDir(Colored('EboundServices Channels','EB',True) ,'ZEMTV' ,10,'', False, True,isItFolder=False)		#name,url,mode,icon
		try:
			AddChannelsFromEbound();#AddChannels()
		except: pass
		addDir(Colored('Other sources','ZM',True) ,'ZEMTV' ,10,'', False, True,isItFolder=False)
		try:
			AddChannelsFromOthers()
		except:
			print 'somethingwrong'
			traceback.print_exc(file=sys.stdout)
	return

def AddChannelsFromOthers():
    main_ch='(<section_name>Pakistani<\/section_name>.*?<\/section>)'
    patt='<channel><channel_number>.*?<channel_name>(.+?[^<])</channel_name><channel_type>(.+?)</channel_type>.*?[^<"]<channel_url>(.*?)</channel_url></channel>'
    url="http://ferrarilb.jemtv.com/index.php/2_2/gxml/channel_list/1"
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()

    match =re.findall(main_ch,link)[0]
    match =re.findall(patt,match)
    if not any('News One' == x[0] for x in match):
        match.append(('News One','manual','http://dag.total-stream.net/dag1.asx?id=ad1!newsone'))
    match.append(('Ary news (manual)','manual','http://dag.total-stream.net/dag1.asx?id=ad1!arynews'))
    match.append(('Express news (manual)','manual','http://dag.total-stream.net/dag1.asx?id=ad1!expressnews'))
    match.append(('Geo news (manual)','manual','http://dag.total-stream.net/dag1.asx?id=jdp!geonewsap'))
    match.append(('Ary Zindagi','manual','http://live.aryzindagi.tv/'))
    match.append(('ETV Urdu','manual','etv'))
    match.append(('Tez','manual','http://dag.total-stream.net/dag1.asx?id=ad1!tez'))

    match.append((base64.b64decode('U2t5IFNwb3J0IDE='),'manual',base64.b64decode('aHR0cDovL2pweG1sLmphZG9vdHYuY29tL3Z1eG1sLnBocC9qYWRvb3htbDMvcGxheS8zMTY=')))

    match.append((base64.b64decode('U2t5IFNwb3J0IDI='),'manual',base64.b64decode('aHR0cDovL2pweG1sLmphZG9vdHYuY29tL3Z1eG1sLnBocC9qYWRvb3htbDMvcGxheS8zMjY=')))

    match.append((base64.b64decode('U2t5IFNwb3J0IDQ='),'manual',base64.b64decode('aHR0cDovL2pweG1sLmphZG9vdHYuY29tL3Z1eG1sLnBocC9qYWRvb3htbDMvcGxheS8zMTU=')))

##other v2
    match.append((base64.b64decode('U2tpIFNwb3J0IDEgVjI='),'manual',base64.b64decode('aHR0cDovL2FjYWJzdy5kb2lwdHYuY29tL3NreV9zcG9ydF8xL3BsYXlsaXN0Lm0zdTh8VXNlci1BZ2VudD1MYXZmNTMuMzIuMTAw')))
    match.append((base64.b64decode('U2tpIFNwb3J0IDIgVjI='),'manual',base64.b64decode('aHR0cDovL2FjYWJzdy5kb2lwdHYuY29tL3NreV9zcG9ydF8yL3BsYXlsaXN0Lm0zdTh8VXNlci1BZ2VudD1MYXZmNTMuMzIuMTAw')))
    match.append((base64.b64decode('U2tpIFNwb3J0IDMgVjI='),'manual',base64.b64decode('aHR0cDovL2FjYWJzdy5kb2lwdHYuY29tL3NreV9zcG9ydF8yL3BsYXlsaXN0Lm0zdTh8VXNlci1BZ2VudD1MYXZmNTMuMzIuMTAw')))
    match.append((base64.b64decode('U2tpIFNwb3J0IDQgVjI='),'manual',base64.b64decode('aHR0cDovL2FjYWJzdy5kb2lwdHYuY29tL3NreV9zcG9ydF80L3BsYXlsaXN0Lm0zdTh8VXNlci1BZ2VudD1MYXZmNTMuMzIuMTAw')))
    match.append((base64.b64decode('U2tpIFNwb3J0IDUgVjI='),'manual',base64.b64decode('aHR0cDovL2FjYWJzdy5kb2lwdHYuY29tL3NreV9zcG9ydF81L3BsYXlsaXN0Lm0zdTh8VXNlci1BZ2VudD1MYXZmNTMuMzIuMTAw')))
    match.append((base64.b64decode('U2tpIFNwb3J0IEYxIFYy'),'manual',base64.b64decode('aHR0cDovL2FjYWJzdy5kb2lwdHYuY29tL3NreV9zcG9ydF9mMS9wbGF5bGlzdC5tM3U4fFVzZXItQWdlbnQ9TGF2ZjUzLjMyLjEwMA==')))




    #for s in [92,104,126,127,133,136,137,168,169,173,177,218,219,230,234,236,242,249,250,251,252,253,262,268,278,280,286,288,307,308,318,336,341,362,363,373,382,404,411,412,417,418,422,428,464,529,531,533,535,537,539,567,569,573,614,620,621,624,625,626,627,628,629,674,676,683,692,693,697,702,703,728,729,745,746,748,752,753,764,840,909,]:
    #    match.append((str(s),'manual','http://ferrarilb.jemtv.com/index.php/2_2/gxml/play/'+str(s)))

    for s in [104,108,109,111,130,131,133,135,136,137,139,140,175,177,179,191,193,204,206,231,234,246,289,296,305,313,314,315,316,317,318,319,320,321,322,323,324,325,326,328,329,330,331,332,333,334,335,337,338,355,356,368,370,372,373,380,381,400,401,434,435,444,446,452,455,457,458,476,477,487,500,508,509,510,516,517,569,615,617,621,643,645,655,723,732,744,780,784,823,827,872,875,881,907,910,911,912,913]:
        match.append(('ZZTest '+str(s),'manual',base64.b64decode('aHR0cDovL2pweG1sLmphZG9vdHYuY29tL3Z1eG1sLnBocC9qYWRvb3htbDMvcGxheS8=')+str(s)))


#    match=sorted(match,key=itemgetter(0)   )
    match=sorted(match,key=lambda s: s[0].lower()   )
    for cname, ctype,curl in match:
        if ctype<>'liveWMV':
            addDir(Colored(cname.capitalize(),'ZM') ,curl ,11,'', False, True,isItFolder=False)		#name,url,mode,icon
    return
    
def re_me(data, re_patten):
    match = ''
    m = re.search(re_patten, data)
    if m != None:
        match = m.group(1)
    else:
        match = ''
    return match

def revist_dag(page_data):
    final_url = ''
    if '127.0.0.1' in page_data:
        final_url = re_me(page_data, '&ver_t=([^&]+)&') + ' live=true timeout=15 playpath=' + re_me(page_data, '\\?y=([a-zA-Z0-9-_\\.@]+)')
    if re_me(page_data, 'token=([^&]+)&') != '':
        final_url = final_url + '?token=' + re_me(page_data, 'token=([^&]+)&')
    elif re_me(page_data, 'wmsAuthSign%3D([^%&]+)') != '':
        final_url = re_me(page_data, '&ver_t=([^&]+)&') + '?wmsAuthSign=' + re_me(page_data, 'wmsAuthSign%3D([^%&]+)') + '==/mp4:' + re_me(page_data, '\\?y=([^&]+)&')
    else:
        final_url = re_me(page_data, 'HREF="([^"]+)"')

    if 'dag1.asx' in final_url:
        return get_dag_url(final_url)

    if 'devinlivefs.fplive.net' not in final_url:
        final_url = final_url.replace('devinlive', 'flive')
    if 'permlivefs.fplive.net' not in final_url:
        final_url = final_url.replace('permlive', 'flive')
    return final_url

def get_dag_url(page_data):
    print 'get_dag_url',page_data
    if '127.0.0.1' in page_data:
        return revist_dag(page_data)
    elif re_me(page_data, 'wmsAuthSign%3D([^%&]+)') != '':
        final_url = re_me(page_data, '&ver_t=([^&]+)&') + '?wmsAuthSign=' + re_me(page_data, 'wmsAuthSign%3D([^%&]+)') + '==/mp4:' + re_me(page_data, '\\?y=([^&]+)&')
    else:
        final_url = re_me(page_data, 'href="([^"]+)"[^"]+$')
        if len(final_url)==0:
            final_url=page_data
    final_url = final_url.replace(' ', '%20')
    return final_url
    
def PlayOtherUrl ( url ):
    progress = xbmcgui.DialogProgress()
    progress.create('Progress', 'Fetching Streaming Info')
    progress.update( 10, "", "Finding links..", "" )

    if url=='http://live.aryzindagi.tv/':
        req = urllib2.Request(url)
        #req.add_header('User-Agent', 'Verismo-BlackUI_(2.4.7.5.8.0.34)')   
        #req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
        req.add_header('User-Agent', 'Verismo-BlackUI_(2.4.7.5.8.0.34)') 
        response = urllib2.urlopen(req)
        link=response.read()
        curlpatth='file: "(htt.*?)"'
        progress.update( 50, "", "Preparing url..", "" )
        dag_url =re.findall(curlpatth,link)[0]
    elif url=='etv':
        req = urllib2.Request('http://m.news18.com/live-tv/etv-urdu')
        #req.add_header('User-Agent', 'Verismo-BlackUI_(2.4.7.5.8.0.34)')   
        req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
        #req.add_header('User-Agent', 'Verismo-BlackUI_(2.4.7.5.8.0.34)') 
        response = urllib2.urlopen(req)
        link=response.read()
        curlpatth='<source src="(.*?)"'
        progress.update( 50, "", "Preparing url..", "" )
        dag_url =re.findall(curlpatth,link)[0]
    elif 'dag1.asx' not in url and 'Lavf53.32.100' not in url:
        req = urllib2.Request(url)
        #req.add_header('User-Agent', 'Verismo-BlackUI_(2.4.7.5.8.0.34)')   
        #req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
        response = urllib2.urlopen(req)
        link=response.read()
        curlpatth='<link>(.*?)<\/link>'
        progress.update( 50, "", "Preparing url..", "" )
        dag_url =re.findall(curlpatth,link)
        if not (dag_url and len(dag_url)>0 ):
            curlpatth='\<ENTRY\>\<REF HREF="(.*?)"'
            dag_url =re.findall(curlpatth,link)[0]
        else:
            dag_url=dag_url[0]
    else:
        dag_url=url
    print 'dag_url',dag_url,name
    if 'Dunya news' in name and 'dag1.asx' not in dag_url:
        print 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        dag_url='http://dag-chi.totalstream.net/dag1.asx?id=ad1!dunya'

    if 'dag1.asx' in dag_url:    
        

        req = urllib2.Request(dag_url)
        req.add_header('User-Agent', 'Verismo-BlackUI_(2.4.7.5.8.0.34)')   
        response = urllib2.urlopen(req)
        link=response.read()
        dat_pattern='href="([^"]+)"[^"]+$'
        dag_url =re.findall(dat_pattern,link)[0]
    print 'dag_url2',dag_url
    final_url=get_dag_url(dag_url)
    progress.update( 100, "", "Almost done..", "" )
    print final_url
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    print "playing stream name: " + str(name) 
    xbmc.Player( xbmc.PLAYER_CORE_AUTO ).play( final_url, listitem)    

def AddChannelsFromEbound():
	liveURL='http://eboundservices.com/istream_demo.php'
	req = urllib2.Request(liveURL)
	req.add_header('User-Agent','Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
#	print link
#	match=re.compile('<param name="URL" value="(.+?)">').findall(link)
#	match=re.compile('<a href="(.+?)"').findall(link)
#	match=re.compile('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>').findall(link)
#	match =re.findall('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
#	match =re.findall('onclick="playChannel\(\'(.*?)\'\);".?>(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
#	match =re.findall('<div class=\"post-title\"><a href=\"(.*?)\".*<b>(.*)<\/b><\/a>', link, re.IGNORECASE)
#	match =re.findall('<img src="(.*?)" alt=".*".+<\/a>\n*.+<div class="post-title"><a href="(.*?)".*<b>(.*)<\/b>', link, re.UNICODE)

	match =re.findall('<a href=".*?stream=(.*?)".*?src="(.*?)" (.)', link,re.M)

	print match
	expressExists=False
	expressCName='express'
	arynewsAdded=False
	
	if not any('Express Tv' == x[0] for x in match):
		match.append(('Express Tv','express','manual'))
	if not any('Ary News' == x[0] for x in match):
		match.append(('Ary News','arynews','manual'))
	if not any('Ary Digital' == x[0] for x in match):
		match.append(('Ary Digital','aryentertainment','manual'))

	match.append(('Baby Tv','babytv','manual'))
	match.append(('Star Gold','stargold','manual'))
	match.append(('Ten Sports','tensports','manual'))
	match.append(('Discovery','discovery','manual'))
	match.append(('National Geographic','nationalgeographic','manual'))
	match.append(('mecca','mecca','manual'))
	match.append(('madina','madina','manual'))
	match.append(('Qtv','qtv','manual'))
	match.append(('Peace Tv','peacetv','manual'))

	match=sorted(match,key=lambda s: s[0].lower()   )

	#h = HTMLParser.HTMLParser()
	for cname in match:
		if cname[2]=='manual':
			addDir(Colored(cname[0].capitalize(),'EB') ,cname[1] ,9,cname[2], False, True,isItFolder=False)		#name,url,mode,icon
		else:
			addDir(Colored(cname[0].capitalize(),'EB') ,cname[0] ,9,cname[1], False, True,isItFolder=False)		#name,url,mode,icon

		if 1==2:
			if cname[0]==expressCName:
				expressExists=True
			if cname[0]=='arynews':
				arynewsAdded=True

	if 1==2:			
		if not expressExists:
			addDir(Colored('Express Tv','EB') ,'express' ,9,'', False, True,isItFolder=False)		#name,url,mode,icon
		if not arynewsAdded:
			addDir(Colored('Ary News','EB') ,'arynews' ,9,'', False, True,isItFolder=False)		#name,url,mode,icon
			addDir(Colored('Ary Digital','EB') ,'aryentertainment' ,9,'', False, True,isItFolder=False)		#name,url,mode,icon
		addDir(Colored('Baby Tv','EB') ,'babytv' ,9,'', False, True,isItFolder=False)		#name,url,mode,icon
		addDir(Colored('Star Gold','EB') ,'stargold' ,9,'', False, True,isItFolder=False)		#name,url,mode,icon
		addDir(Colored('Ten Sports','EB') ,'tensports' ,9,'', False, True,isItFolder=False)		#name,url,mode,icon
	return		

def Colored(text = '', colorid = '', isBold = False):
	if colorid == 'ZM':
		color = 'FF11b500'
	elif colorid == 'EB':
		color = 'FFe37101'
	elif colorid == 'bold':
		return '[B]' + text + '[/B]'
	else:
		color = colorid
		
	if isBold == True:
		text = '[B]' + text + '[/B]'
	return '[COLOR ' + color + ']' + text + '[/COLOR]'	

def PlayShowLinkDup ( url ): 
#	url = tabURL.replace('%s',channelName);
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
#	print url

	line1 = "Playing DM Link"
	time = 5000  #in miliseconds
 	defaultLinkType=0 #0 youtube,1 DM,2 tunepk
	defaultLinkType=selfAddon.getSetting( "DefaultVideoType" ) 
	#print defaultLinkType
	#print "LT link is" + linkType
	# if linktype is not provided then use the defaultLinkType
	linkType="LINK"
	if linkType=="DM" or (linkType=="" and defaultLinkType=="1"):
		print "PlayDM"
		line1 = "Playing DM Link"
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
#		print link
		playURL= match =re.findall('src="(.*?(dailymotion).*?)"',link)
		playURL=match[0][0]
		print playURL
		playlist = xbmc.PlayList(1)
		playlist.clear()
		listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
		listitem.setInfo("Video", {"Title":name})
		listitem.setProperty('mimetype', 'video/x-msvideo')
		listitem.setProperty('IsPlayable', 'true')
		stream_url = urlresolver.HostedMediaFile(playURL).resolve()
		print stream_url
		playlist.add(stream_url,listitem)
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
	        xbmcPlayer.play(playlist)
#src="(.*?(dailymotion).*?)"
	elif  linkType=="LINK"  or (linkType=="" and defaultLinkType=="2"):
		line1 = "Playing Tune.pk Link"
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))

		print "PlayLINK"
		playURL= match =re.findall('<strong>Tune Full<\/strong>\s*.*?src="(.*?(tune\.pk).*?)"', link)
		playURL=match[0][0]# check if not found then try other methods
		print playURL
		playlist = xbmc.PlayList(1)
		playlist.clear()
		listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
		listitem.setInfo("Video", {"Title":name})
		listitem.setProperty('mimetype', 'video/x-msvideo')
		listitem.setProperty('IsPlayable', 'true')
		stream_url = urlresolver.HostedMediaFile(playURL).resolve()
		print stream_url
		playlist.add(stream_url,listitem)
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
	        xbmcPlayer.play(playlist)

#src="(.*?(tune\.pk).*?)"
	else:	#either its default or nothing selected
		line1 = "Playing Youtube Link"
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))

		youtubecode= match =re.findall('<strong>Youtube<\/strong>.*?src=\".*?embed\/(.*?)\?.*\".*?<\/iframe>', link,re.DOTALL| re.IGNORECASE)
		youtubecode=youtubecode[0]
		uurl = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % youtubecode
#	print uurl
		xbmc.executebuiltin("xbmc.PlayMedia("+uurl+")")
	
	return

def AddShows(Fromurl):
#	print Fromurl
	req = urllib2.Request(Fromurl)
	req.add_header('User-Agent','Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
#	print link
#	print "addshows"
#	match=re.compile('<param name="URL" value="(.+?)">').findall(link)
#	match=re.compile('<a href="(.+?)"').findall(link)
#	match=re.compile('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>').findall(link)
#	match =re.findall('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
#	match =re.findall('onclick="playChannel\(\'(.*?)\'\);".?>(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
#	match =re.findall('<div class=\"post-title\"><a href=\"(.*?)\".*<b>(.*)<\/b><\/a>', link, re.IGNORECASE)
#	match =re.findall('<img src="(.*?)" alt=".*".+<\/a>\n*.+<div class="post-title"><a href="(.*?)".*<b>(.*)<\/b>', link, re.UNICODE)

	match =re.findall('<div class="thumbnail">\s*<a href="(.*?)" title="(.*?)".*\s*.*src="(.*?)"', link, re.UNICODE)
#	print Fromurl

#	print match
	h = HTMLParser.HTMLParser()

	for cname in match:
		addDir(h.unescape(cname[1]) ,cname[0] ,3,cname[2], True,isItFolder=False)
		
#	<a href="http://www.zemtv.com/page/2/">&gt;</a></li>
	match =re.findall('<a class="nextpostslink" rel="next" href="(.*?)">', link, re.IGNORECASE)
	
	if len(match)==1:
		addDir('Next Page' ,match[0] ,2,'',isItFolder=True)
#       print match
	
	return

	
def AddChannels():
	req = urllib2.Request(liveURL)
	req.add_header('User-Agent','Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
#	print link
#	match=re.compile('<param name="URL" value="(.+?)">').findall(link)
#	match=re.compile('<a href="(.+?)"').findall(link)
#	match=re.compile('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>').findall(link)
#	match =re.findall('onclick="playChannel\(\'(.*?)\'\);">(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
#	match =re.findall('onclick="playChannel\(\'(.*?)\'\);".?>(.*?)</a>', link, re.DOTALL|re.IGNORECASE)
#	match =re.findall('<div class=\"post-title\"><a href=\"(.*?)\".*<b>(.*)<\/b><\/a>', link, re.IGNORECASE)
#	match =re.findall('<img src="(.*?)" alt=".*".+<\/a>\n*.+<div class="post-title"><a href="(.*?)".*<b>(.*)<\/b>', link, re.UNICODE)

	match =re.findall('<div class="epic-cs">\s*<a href="(.+)" rel=.*<img src="(.+)" alt="(.+)" \/>', link, re.UNICODE)

#	print match
	h = HTMLParser.HTMLParser()
	for cname in match:
		addDir(Colored(h.unescape(cname[2].replace("Watch Now Watch ","").replace("Live, High Quality Streaming","").replace("Live &#8211; High Quality Streaming","").replace("Watch Now ","")) ,'ZM'),cname[0] ,4,cname[1],False,True,isItFolder=False)		
	return	

	
	

def PlayShowLink ( url ): 
#	url = tabURL.replace('%s',channelName);
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
#	print url

	line1 = "Playing DM Link"
	time = 5000  #in miliseconds
 	defaultLinkType=0 #0 youtube,1 DM,2 tunepk
	defaultLinkType=selfAddon.getSetting( "DefaultVideoType" ) 
	print defaultLinkType
	print "LT link is" + linkType
	# if linktype is not provided then use the defaultLinkType
	
	if linkType.upper()=="SHOWALL" or (linkType.upper()=="" and defaultLinkType=="5"):
		ShowAllSources(url,link)
		return
	if linkType.upper()=="DM" or (linkType=="" and defaultLinkType=="1"):
		print "PlayDM"
		line1 = "Playing DM Link"
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
#		print link
		playURL= match =re.findall('src="(.*?(dailymotion).*?)"',link)
		if len(playURL)==0:
			line1 = "Daily motion link not found"
			xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
			ShowAllSources(url,link)
			return 
		playURL=match[0][0]
		print playURL
		playlist = xbmc.PlayList(1)
		playlist.clear()
		listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
		listitem.setInfo("Video", {"Title":name})
		listitem.setProperty('mimetype', 'video/x-msvideo')
		listitem.setProperty('IsPlayable', 'true')
		stream_url = urlresolver.HostedMediaFile(playURL).resolve()
		print stream_url
		playlist.add(stream_url,listitem)
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)
		#xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
		#src="(.*?(dailymotion).*?)"
	elif  linkType.upper()=="EBOUND"  or (linkType=="" and defaultLinkType=="4"):
		line1 = "Playing Ebound Link"
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
		print "Eboundlink"
		playURL= match =re.findall(' src=".*?ebound\\.tv.*?site=(.*?)&.*?date=(.*?)\\&', link)
		if len(playURL)==0:
			line1 = "EBound link not found"
			xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
			ShowAllSources(url,link)
			return 

		playURL=match[0]
		dt=playURL[1]
		clip=playURL[0]
		urli='http://www.eboundservices.com/iframe/new/vod_ugc.php?stream=mp4:vod/%s/%s&width=620&height=350&clip=%s&day=%s&month=undefined'%(dt,clip,clip,dt)
		#req = urllib2.Request(urli)
		#req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
		#response = urllib2.urlopen(req)
		#link=response.read()
		#response.close()
		post = {'username':'hash'}
		post = urllib.urlencode(post)
		req = urllib2.Request('http://eboundservices.com/flashplayerhash/index.php')
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36')
		response = urllib2.urlopen(req,post)
		link=response.read()
		response.close()
		strval =link;# match[0]

		stream_url='rtmp://cdn.ebound.tv/vod playpath=mp4:vod/%s/%s app=vod?wmsAuthSign=%s swfurl=http://www.eboundservices.com/live/v6/player.swf?domain=www.zemtv.com&channel=%s&country=EU pageUrl=%s tcUrl=rtmp://cdn.ebound.tv/vod?wmsAuthSign=%s live=true timeout=15'	% (dt,clip,strval,clip,urli,strval)

		print stream_url
		playlist = xbmc.PlayList(1)
		playlist.clear()
		listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
		listitem.setInfo("Video", {"Title":name})
		listitem.setProperty('mimetype', 'video/x-msvideo')
		listitem.setProperty('IsPlayable', 'true')
		playlist.add(stream_url,listitem)
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)
	elif  linkType.upper()=="LINK"  or (linkType=="" and defaultLinkType=="2"):
		line1 = "Playing Tune.pk Link"
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
		print "PlayLINK"
		playURL= match =re.findall('src="(.*?(tune\.pk).*?)"', link)
		if len(playURL)==0:
			line1 = "Link.pk link not found"
			xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
			ShowAllSources(url,link)
			return 

		playURL=match[0][0]
		print playURL
		playlist = xbmc.PlayList(1)
		playlist.clear()
		listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
		listitem.setInfo("Video", {"Title":name})
		listitem.setProperty('mimetype', 'video/x-msvideo')
		listitem.setProperty('IsPlayable', 'true')
		stream_url = urlresolver.HostedMediaFile(playURL).resolve()
		print stream_url
		playlist.add(stream_url,listitem)
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)
	elif  linkType.upper()=="PLAYWIRE"  or (linkType=="" and defaultLinkType=="3"):
		line1 = "Playing Playwire Link"
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
		print "Playwire"
		playURL =re.findall('src=".*?(playwire).*?data-publisher-id="(.*?)"\s*data-video-id="(.*?)"', link)
		V=1
		if len(playURL)==0:
			playURL =re.findall('data-config="(.*?config.playwire.com.*?)"', link)
			V=2
		if len(playURL)==0:
			line1 = "Playwire link not found"
			xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
			ShowAllSources(url,link)
			return 
		if V==1:
			(playWireVar,PubId,videoID)=playURL[0]
			cdnUrl="http://cdn.playwire.com/v2/%s/config/%s.json"%(PubId,videoID)
			req = urllib2.Request(cdnUrl)
			req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
			response = urllib2.urlopen(req)
			link=response.read()
			response.close()
			playURL ="http://cdn.playwire.com/%s/%s"%(PubId,re.findall('src":".*?mp4:(.*?)"', link)[0])
			print 'playURL',playURL
		else:
			playURL=playURL[0]
			reg='media":\{"(.*?)":"(.*?)"'
			req = urllib2.Request(playURL)
			req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
			response = urllib2.urlopen(req)
			link=response.read()
			playURL =re.findall(reg, link)
			if len(playURL)>0:
				playURL=playURL[0]
				ty=playURL[0]
				innerUrl=playURL[1]
				print innerUrl
				req = urllib2.Request(innerUrl)
				req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
				response = urllib2.urlopen(req)
				link=response.read()
				reg='baseURL>(.*?)<\/baseURL>\s*?<media url="(.*?)"'
				playURL =re.findall(reg, link)[0]
				playURL=playURL[0]+'/'+playURL[1]
		playlist = xbmc.PlayList(1)
		playlist.clear()
		listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
		listitem.setInfo("Video", {"Title":name})
		listitem.setProperty('mimetype', 'video/x-msvideo')
		listitem.setProperty('IsPlayable', 'true')
		stream_url = playURL#urlresolver.HostedMediaFile(playURL).resolve()
		print 'stream_url',stream_url
		playlist.add(stream_url,listitem)
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)
		#bmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)#src="(.*?(tune\.pk).*?)"
	else:	#either its default or nothing selected
		line1 = "Playing Youtube Link"
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
		youtubecode= match =re.findall('<strong>Youtube<\/strong>.*?src=\".*?embed\/(.*?)\?.*\".*?<\/iframe>', link,re.DOTALL| re.IGNORECASE)
		if len(youtubecode)==0:
			line1 = "Youtube link not found"
			xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
			ShowAllSources(url,link)
			return
		youtubecode=youtubecode[0]
		uurl = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % youtubecode
#	print uurl
		xbmc.executebuiltin("xbmc.PlayMedia("+uurl+")")
	
	return

def ShowAllSources(url, loadedLink=None):
	global linkType
	print 'show all sources',url
	link=loadedLink
	if not loadedLink:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
	available_source=[]
	playURL =re.findall('src=".*?(playwire).*?data-publisher-id="(.*?)"\s*data-video-id="(.*?)"', link)
	print 'playURL',playURL
	if not len(playURL)==0:
		available_source.append('Playwire Source')

	playURL =re.findall('data-config="(.*?config.playwire.com.*?)"', link)
	print 'playURL',playURL
	if not len(playURL)==0:
		available_source.append('Playwire Source')

	playURL =re.findall('src="(.*?ebound\\.tv.*?)"', link)
	print 'playURL',playURL
	if not len(playURL)==0:
		available_source.append('Ebound Source')		
		 
	playURL= match =re.findall('src="(.*?(dailymotion).*?)"',link)
	if not len(playURL)==0:
		available_source.append('Daily Motion Source')

	playURL= match =re.findall('src="(.*?(tune\.pk).*?)"', link)
	if not len(playURL)==0:
		available_source.append('Link Source')

	playURL= match =re.findall('<strong>Youtube<\/strong>.*?src=\".*?embed\/(.*?)\?.*\".*?<\/iframe>', link,re.DOTALL| re.IGNORECASE)
	if not len(playURL)==0:
		available_source.append('Youtube Source')

	if len(available_source)>0:
		dialog = xbmcgui.Dialog()
		index = dialog.select('Choose your stream', available_source)
		if index > -1:
			linkType=available_source[index].replace(' Source','').replace('Daily Motion','DM').upper()
			print 'linkType',linkType
			PlayShowLink(url);

def PlayLiveLink ( url ):
	progress = xbmcgui.DialogProgress()
	progress.create('Progress', 'Fetching Streaming Info')
	progress.update( 10, "", "Finding links..", "" )
	if mode==4:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		#print link
		#print url
		match =re.findall('"http.*(ebound).*?\?site=(.*?)"',link,  re.IGNORECASE)[0]
		cName=match[1]
		progress.update( 20, "", "Finding links..", "" )
	else:
		cName=url
	import math, random, time
	rv=str(int(5000+ math.floor(random.random()*10000)))
	currentTime=str(int(time.time()*1000))
	#newURL='http://www.eboundservices.com/iframe/newads/iframe.php?stream='+ cName+'&width=undefined&height=undefined&clip=' + cName
	newURL='http://www.eboundservices.com/iframe/new/mainPage.php?stream='+cName+  '&width=undefined&height=undefined&clip=' + cName+'&rv='+rv+'&_='+currentTime
	
	req = urllib2.Request(newURL)
	req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	progress.update( 50, "", "Finding links..", "" )
	
#	match =re.findall('<iframe.+src=\'(.*)\' frame',link,  re.IGNORECASE)
#	print match
#	req = urllib2.Request(match[0])
#	req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
#	response = urllib2.urlopen(req)
#	link=response.read()
#	response.close()
	time = 2000  #in miliseconds
	defaultStreamType=0 #0 RTMP,1 HTTP
	defaultStreamType=selfAddon.getSetting( "DefaultStreamType" ) 
	print 'defaultStreamType',defaultStreamType
	if 1==2 and (linkType=="HTTP" or (linkType=="" and defaultStreamType=="1")): #disable http streaming for time being
#	print link
		line1 = "Playing Http Stream"
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
		
		match =re.findall('MM_openBrWindow\(\'(.*)\',\'ebound\'', link,  re.IGNORECASE)
			
	#	print url
	#	print match
		
		strval = match[0]
		
		#listitem = xbmcgui.ListItem(name)
		#listitem.setInfo('video', {'Title': name, 'Genre': 'Live TV'})
		#playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
		#playlist.clear()
		#playlist.add (strval)
		
		#xbmc.Player().play(playlist)
		listitem = xbmcgui.ListItem( label = str(cName), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ), path=strval )
		print "playing stream name: " + str(cName) 
		listitem.setInfo( type="video", infoLabels={ "Title": cName, "Path" : strval } )
		listitem.setInfo( type="video", infoLabels={ "Title": cName, "Plot" : cName, "TVShowTitle": cName } )
		xbmc.Player(PLAYER_CORE_AUTO).play( str(strval), listitem)
	else:
		line1 = "Playing RTMP Stream"
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
		progress.update( 60, "", "Finding links..", "" )
		post = {'username':'hash'}
        	post = urllib.urlencode(post)
		req = urllib2.Request('http://eboundservices.com/flashplayerhash/index.php')
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36')
		response = urllib2.urlopen(req,post)
		link=response.read()
		response.close()
		

        
		print link
		#match =re.findall("=(.*)", link)

		#print url
		#print match

		strval =link;# match[0]

		#listitem = xbmcgui.ListItem(name)
		#listitem.setInfo('video', {'Title': name, 'Genre': 'Live TV'})
		#playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
		#playlist.clear()
		#playlist.add (strval)

		playfile='rtmp://cdn.ebound.tv/tv?wmsAuthSign=/%s app=tv?wmsAuthSign=%s swfurl=http://www.eboundservices.com/live/v6/jwplayer.flash.swf?domain=www.eboundservices.com&channel=%s&country=EU pageUrl=http://www.eboundservices.com/channel.php?app=tv&stream=%s tcUrl=rtmp://cdn.ebound.tv/tv?wmsAuthSign=%s live=true timeout=15'	% (cName,strval,cName,cName,strval)
		#playfile='rtmp://cdn.ebound.tv/tv?wmsAuthSign=/humtv app=tv?wmsAuthSign=?%s swfurl=http://www.eboundservices.com/live/v6/player.swf?domain=&channel=humtv&country=GB pageUrl=http://www.eboundservices.com/iframe/newads/iframe.php?stream=humtv tcUrl=rtmp://cdn.ebound.tv/tv?wmsAuthSign=?%s live=true'	% (strval,strval)
		progress.update( 100, "", "Almost done..", "" )
		print playfile
		#xbmc.Player().play(playlist)
		listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
		print "playing stream name: " + str(name) 
		#listitem.setInfo( type="video", infoLabels={ "Title": name, "Path" : playfile } )
		#listitem.setInfo( type="video", infoLabels={ "Title": name, "Plot" : name, "TVShowTitle": name } )
		xbmc.Player( xbmc.PLAYER_CORE_AUTO ).play( playfile, listitem)
		#xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
	
	
	return


#print "i am here"
params=get_params()
url=None
name=None
mode=None
linkType=None

try:
	url=urllib.unquote_plus(params["url"])
except:
	pass
try:
	name=urllib.unquote_plus(params["name"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	pass


args = cgi.parse_qs(sys.argv[2][1:])
linkType=''
try:
	linkType=args.get('linkType', '')[0]
except:
	pass


print 	mode,url,linkType

try:
	if mode==None or url==None or len(url)<1:
		print "InAddTypes"
		Addtypes()
	elif mode==2:
		print "Ent url is "+name
		AddEnteries(name)

	elif mode==3:
		print "Play url is "+url
		PlayShowLink(url)

	elif mode==4 or mode==9:
		print "Play url is "+url
		PlayLiveLink(url)
	elif mode==11:
		print "Play url is "+url
		PlayOtherUrl(url)

	elif mode==6 :
		print "Play url is "+url
		ShowSettings(url)
except:
	print 'somethingwrong'
	traceback.print_exc(file=sys.stdout)
	

if not ( (mode==3 or mode==4 or mode==9 )  )  :
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
