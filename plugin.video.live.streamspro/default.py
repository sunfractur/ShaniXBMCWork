# -*- coding: utf-8 -*-

import urllib
import urllib2
import datetime
import re
import os
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs
import traceback
import cookielib
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP
try:
    import json
except:
    import simplejson as json
import SimpleDownloader as downloader
import time
import requests

resolve_url=['180upload', 'my.mail.ru','streamin.to', '2gbhosting', 'alldebrid', 'allmyvideos', 'auengine', 'bayfiles', 'bestreams', 'billionuploads', 'castamp', 'cheesestream', 'clicktoview', 'cloudy', 'crunchyroll', 'cyberlocker', 'daclips', 'dailymotion', 'divxstage', 'donevideo', 'ecostream', 'entroupload', 'exashare', 'facebook', 'filebox', 'filenuke', 'flashx', 'gorillavid', 'hostingbulk', 'hostingcup', 'hugefiles', 'jumbofiles', 'lemuploads', 'limevideo', 'megarelease', 'megavids', 'mightyupload', 'mooshare_biz', 'movdivx', 'movpod', 'movreel', 'movshare', 'movzap', 'mp4stream', 'mp4upload', 'mrfile', 'muchshare', 'nolimitvideo', 'nosvideo', 'novamov', 'nowvideo', 'ovfile', 'play44_net', 'played', 'playwire', 'premiumize_me', 'primeshare', 'promptfile', 'purevid', 'putlocker', 'rapidvideo', 'realdebrid', 'rpnet', 'seeon', 'sharedsx', 'sharefiles', 'sharerepo', 'sharesix', 'sharevid', 'skyload', 'slickvid', 'sockshare', 'stagevu', 'stream2k', 'streamcloud', 'teramixer', 'thefile', 'thevideo', 'trollvid', 'tubeplus', 'tunepk', 'ufliq', 'uploadc', 'uploadcrazynet', 'veeHD', 'veoh', 'vidbull', 'vidcrazynet', 'video44', 'videobb', 'videoboxone', 'videofun', 'videomega', 'videoraj', 'videotanker', 'videovalley', 'videoweed', 'videozed', 'videozer', 'vidhog', 'vidpe', 'vidplay', 'vidspot', 'vidstream', 'vidto', 'vidup_org', 'vidxden', 'vidzi', 'vidzur', 'vimeo', 'vk', 'vodlocker', 'vureel', 'watchfreeinhd', 'xvidstage', 'yourupload', 'youwatch', 'zalaa', 'zooupload', 'zshare']
g_ignoreSetResolved=['plugin.video.f4mTester','plugin.video.shahidmbcnet','plugin.video.SportsDevil','plugin.stream.vaughnlive.tv']

REMOTE_DBG=False;
if REMOTE_DBG:
    # Make pydev debugger works for auto reload.
    # Note pydevd module need to be copied in XBMC\system\python\Lib\pysrc
    try:
        import pysrc.pydevd as pydevd
    # stdoutToServer and stderrToServer redirect stdout and stderr to eclipse console
        pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True)
    except ImportError:
        sys.stderr.write("Error: " +
            "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")
        sys.exit(1)  


addon = xbmcaddon.Addon('plugin.video.live.streamspro')
addon_version = addon.getAddonInfo('version')
profile = xbmc.translatePath(addon.getAddonInfo('profile').decode('utf-8'))
home = xbmc.translatePath(addon.getAddonInfo('path').decode('utf-8'))
favorites = os.path.join(profile, 'favorites')
history = os.path.join(profile, 'history')

REV = os.path.join(profile, 'list_revision')
icon = os.path.join(home, 'icon.png')
FANART = os.path.join(home, 'fanart.jpg')
source_file = os.path.join(profile, 'source_file')
functions_dir = profile

downloader = downloader.SimpleDownloader()
debug = addon.getSetting('debug')
if os.path.exists(favorites)==True:
    FAV = open(favorites).read()
else: FAV = []
if os.path.exists(source_file)==True:
    SOURCES = open(source_file).read()
else: SOURCES = []


def addon_log(string):
    if debug == 'true':
        xbmc.log("[addon.live.streamspro-%s]: %s" %(addon_version, string))


def makeRequest(url, headers=None):
        try:
            if headers is None:
                headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0'}
            req = urllib2.Request(url,None,headers)
            response = urllib2.urlopen(req)
            data = response.read()
            response.close()
            return data
        except urllib2.URLError, e:
            addon_log('URL: '+url)
            if hasattr(e, 'code'):
                addon_log('We failed with error code - %s.' % e.code)
                xbmc.executebuiltin("XBMC.Notification(LiveStreamsPro,We failed with error code - "+str(e.code)+",10000,"+icon+")")
            elif hasattr(e, 'reason'):
                addon_log('We failed to reach a server.')
                addon_log('Reason: %s' %e.reason)
                xbmc.executebuiltin("XBMC.Notification(LiveStreamsPro,We failed to reach a server. - "+str(e.reason)+",10000,"+icon+")")


def getSources():
        if os.path.exists(favorites) == True:
            addDir('Favorites','url',4,os.path.join(home, 'resources', 'favorite.png'),FANART,'','','','')
        if addon.getSetting("browse_xml_database") == "true":
            addDir('XML Database','http://xbmcplus.xb.funpic.de/www-data/filesystem/',15,icon,FANART,'','','','')
        if addon.getSetting("browse_community") == "true":
            addDir('Community Files','community_files',16,icon,FANART,'','','','')
        if os.path.exists(history) == True:
            addDir('Search History','history',25,os.path.join(home, 'resources', 'favorite.png'),FANART,'','','','')
        if addon.getSetting("searchyt") == "true":
            addDir('Search:Youtube','youtube',25,icon,FANART,'','','','')
        if addon.getSetting("searchDM") == "true":
            addDir('Search:dailymotion','dmotion',25,icon,FANART,'','','','')
        if addon.getSetting("PulsarM") == "true":
            addDir('Pulsar:IMDB','IMDBidplay',27,icon,FANART,'','','','')            
        if os.path.exists(source_file)==True:
            sources = json.loads(open(source_file,"r").read())
            #print 'sources',sources
            if len(sources) > 1:
                for i in sources:
                    ## for pre 1.0.8 sources
                    if isinstance(i, list):
                        addDir(i[0].encode('utf-8'),i[1].encode('utf-8'),1,icon,FANART,'','','','','source')
                    else:
                        thumb = icon
                        fanart = FANART
                        desc = ''
                        date = ''
                        credits = ''
                        genre = ''
                        if i.has_key('thumbnail'):
                            thumb = i['thumbnail']
                        if i.has_key('fanart'):
                            fanart = i['fanart']
                        if i.has_key('description'):
                            desc = i['description']
                        if i.has_key('date'):
                            date = i['date']
                        if i.has_key('genre'):
                            genre = i['genre']
                        if i.has_key('credits'):
                            credits = i['credits']
                        addDir(i['title'].encode('utf-8'),i['url'].encode('utf-8'),1,thumb,fanart,desc,genre,date,credits,'source')

            else:
                if len(sources) == 1:
                    if isinstance(sources[0], list):
                        getData(sources[0][1].encode('utf-8'),FANART)
                    else:
                        getData(sources[0]['url'], sources[0]['fanart'])


def addSource(url=None):
        if url is None:
            if not addon.getSetting("new_file_source") == "":
               source_url = addon.getSetting('new_file_source').decode('utf-8')
            elif not addon.getSetting("new_url_source") == "":
               source_url = addon.getSetting('new_url_source').decode('utf-8')
        else:
            source_url = url
        if source_url == '' or source_url is None:
            return
        addon_log('Adding New Source: '+source_url.encode('utf-8'))

        media_info = None
        #print 'source_url',source_url
        data = getSoup(source_url)
        #print 'source_url',source_url
        if data.find('channels_info'):
            media_info = data.channels_info
        elif data.find('items_info'):
            media_info = data.items_info
        if media_info:
            source_media = {}
            source_media['url'] = source_url
            try: source_media['title'] = media_info.title.string
            except: pass
            try: source_media['thumbnail'] = media_info.thumbnail.string
            except: pass
            try: source_media['fanart'] = media_info.fanart.string
            except: pass
            try: source_media['genre'] = media_info.genre.string
            except: pass
            try: source_media['description'] = media_info.description.string
            except: pass
            try: source_media['date'] = media_info.date.string
            except: pass
            try: source_media['credits'] = media_info.credits.string
            except: pass
        else:
            if '/' in source_url:
                nameStr = source_url.split('/')[-1].split('.')[0]
            if '\\' in source_url:
                nameStr = source_url.split('\\')[-1].split('.')[0]
            if '%' in nameStr:
                nameStr = urllib.unquote_plus(nameStr)
            keyboard = xbmc.Keyboard(nameStr,'Displayed Name, Rename?')
            keyboard.doModal()
            if (keyboard.isConfirmed() == False):
                return
            newStr = keyboard.getText()
            if len(newStr) == 0:
                return
            source_media = {}
            source_media['title'] = newStr
            source_media['url'] = source_url
            source_media['fanart'] = fanart

        if os.path.exists(source_file)==False:
            source_list = []
            source_list.append(source_media)
            b = open(source_file,"w")
            b.write(json.dumps(source_list))
            b.close()
        else:
            sources = json.loads(open(source_file,"r").read())
            sources.append(source_media)
            b = open(source_file,"w")
            b.write(json.dumps(sources))
            b.close()
        addon.setSetting('new_url_source', "")
        addon.setSetting('new_file_source', "")
        xbmc.executebuiltin("XBMC.Notification(LiveStreamsPro,New source added.,5000,"+icon+")")
        if not url is None:
            if 'xbmcplus.xb.funpic.de' in url:
                xbmc.executebuiltin("XBMC.Container.Update(%s?mode=14,replace)" %sys.argv[0])
            elif 'community-links' in url:
                xbmc.executebuiltin("XBMC.Container.Update(%s?mode=10,replace)" %sys.argv[0])
        else: addon.openSettings()


def rmSource(name):
        sources = json.loads(open(source_file,"r").read())
        for index in range(len(sources)):
            if isinstance(sources[index], list):
                if sources[index][0] == name:
                    del sources[index]
                    b = open(source_file,"w")
                    b.write(json.dumps(sources))
                    b.close()
                    break
            else:
                if sources[index]['title'] == name:
                    del sources[index]
                    b = open(source_file,"w")
                    b.write(json.dumps(sources))
                    b.close()
                    break
        xbmc.executebuiltin("XBMC.Container.Refresh")



def get_xml_database(url, browse=False):
        if url is None:
            url = 'http://xbmcplus.xb.funpic.de/www-data/filesystem/'
        soup = BeautifulSoup(makeRequest(url), convertEntities=BeautifulSoup.HTML_ENTITIES)
        for i in soup('a'):
            href = i['href']
            if not href.startswith('?'):
                name = i.string
                if name not in ['Parent Directory', 'recycle_bin/']:
                    if href.endswith('/'):
                        if browse:
                            addDir(name,url+href,15,icon,fanart,'','','')
                        else:
                            addDir(name,url+href,14,icon,fanart,'','','')
                    elif href.endswith('.xml'):
                        if browse:
                            addDir(name,url+href,1,icon,fanart,'','','','','download')
                        else:
                            if os.path.exists(source_file)==True:
                                if name in SOURCES:
                                    addDir(name+' (in use)',url+href,11,icon,fanart,'','','','','download')
                                else:
                                    addDir(name,url+href,11,icon,fanart,'','','','','download')
                            else:
                                addDir(name,url+href,11,icon,fanart,'','','','','download')


def getCommunitySources(browse=False):
        url = 'http://community-links.googlecode.com/svn/trunk/'
        soup = BeautifulSoup(makeRequest(url), convertEntities=BeautifulSoup.HTML_ENTITIES)
        files = soup('ul')[0]('li')[1:]
        for i in files:
            name = i('a')[0]['href']
            if browse:
                addDir(name,url+name,1,icon,fanart,'','','','','download')
            else:
                addDir(name,url+name,11,icon,fanart,'','','','','download')


def getSoup(url,data=None):
        if url.startswith('http://') or url.startswith('https://'):
            data = makeRequest(url)
            if re.search("#EXTM3U",data) or 'm3u' in url: 
                print 'found m3u data'
                return data
                
        elif data == None:
            if xbmcvfs.exists(url):
                if url.startswith("smb://") or url.startswith("nfs://"):
                    copy = xbmcvfs.copy(url, os.path.join(profile, 'temp', 'sorce_temp.txt'))
                    if copy:
                        data = open(os.path.join(profile, 'temp', 'sorce_temp.txt'), "r").read()
                        xbmcvfs.delete(os.path.join(profile, 'temp', 'sorce_temp.txt'))
                    else:
                        addon_log("failed to copy from smb:")
                else:
                    data = open(url, 'r').read()
                    if re.match("#EXTM3U",data)or 'm3u' in url: 
                        print 'found m3u data'
                        return data
            else:
                addon_log("Soup Data not found!")
                return
        return BeautifulSOAP(data, convertEntities=BeautifulStoneSoup.XML_ENTITIES)


def getData(url,fanart):
    print 'url-getData',url
    soup = getSoup(url)
    #print type(soup)
    if isinstance(soup,BeautifulSOAP):
    #print 'xxxxxxxxxxsoup',soup
        if len(soup('channels')) > 0:
            channels = soup('channel')
            for channel in channels:
#                print channel

                linkedUrl=''
                lcount=0
                try:
                    linkedUrl =  channel('externallink')[0].string
                    lcount=len(channel('externallink'))
                except: pass
                print 'linkedUrl',linkedUrl,lcount
                if lcount>1: linkedUrl=''

                name = channel('name')[0].string
                thumbnail = channel('thumbnail')[0].string
                if thumbnail == None:
                    thumbnail = ''

                try:
                    if not channel('fanart'):
                        if addon.getSetting('use_thumb') == "true":
                            fanArt = thumbnail
                        else:
                            fanArt = fanart
                    else:
                        fanArt = channel('fanart')[0].string
                    if fanArt == None:
                        raise
                except:
                    fanArt = fanart

                try:
                    desc = channel('info')[0].string
                    if desc == None:
                        raise
                except:
                    desc = ''

                try:
                    genre = channel('genre')[0].string
                    if genre == None:
                        raise
                except:
                    genre = ''

                try:
                    date = channel('date')[0].string
                    if date == None:
                        raise
                except:
                    date = ''

                try:
                    credits = channel('credits')[0].string
                    if credits == None:
                        raise
                except:
                    credits = ''

                try:
                    if linkedUrl=='':
                        addDir(name.encode('utf-8', 'ignore'),url.encode('utf-8'),2,thumbnail,fanArt,desc,genre,date,credits,True)
                    else:
                        #print linkedUrl
                        addDir(name.encode('utf-8'),linkedUrl.encode('utf-8'),1,thumbnail,fanArt,desc,genre,date,None,'source')
                except:
                    addon_log('There was a problem adding directory from getData(): '+name.encode('utf-8', 'ignore'))
        else:
            addon_log('No Channels: getItems')
            getItems(soup('item'),fanart)
    else:
        parse_m3u(soup)
# borrow from https://github.com/enen92/P2P-Streams-XBMC/blob/master/plugin.video.p2p-streams/resources/core/livestreams.py
# This will not go through the getItems functions ( means you must have ready to play url, no regex)
def parse_m3u(data):
    content = data.rstrip()
    match = re.compile(r'#EXTINF:(.+?),(.*?)[\n\r]+([^\n]+)').findall(content)
    total = len(match)
    print 'total m3u links',total
    for other,channel_name,stream_url in match:
        if 'tvg-logo' in other:
            thumbnail = re_me(other,'tvg-logo=[\'"](.*?)[\'"]')
            if thumbnail:
                if thumbnail.startswith('http'):
                    thumbnail = thumbnail
                
                elif not addon.getSetting('logo-folderPath') == "":
                    logo_url = addon.getSetting('logo-folderPath')
                    thumbnail = logo_url + thumbnail

                else:
                    thumbnail = thumbnail
            #else:
            
        else:
            thumbnail = ''
        if 'type' in other:
            mode_type = re_me(other,'type=[\'"](.*?)[\'"]')
            print mode_type
            if mode_type == 'yt-dl':
                stream_url = stream_url +"&mode=18"
            elif mode_type == 'regex':
                url = stream_url.split('&regexs=')
                #print url[0] getSoup(url,data=None)
                regexs = parse_regex(getSoup('',data=url[1]))
                
                addLink(url[0], channel_name.encode('utf-8', 'ignore'),thumbnail,'','','','','',None,regexs,total)
                continue
        addLink(stream_url, channel_name.encode('utf-8', 'ignore'),thumbnail,'','','','','',None,'',total)
def getChannelItems(name,url,fanart):
        soup = getSoup(url)
        channel_list = soup.find('channel', attrs={'name' : name.decode('utf-8')})
        items = channel_list('item')
        try:
            fanArt = channel_list('fanart')[0].string
            if fanArt == None:
                raise
        except:
            fanArt = fanart
        for channel in channel_list('subchannel'):
            name = channel('name')[0].string
            try:
                thumbnail = channel('thumbnail')[0].string
                if thumbnail == None:
                    raise
            except:
                thumbnail = ''
            try:
                if not channel('fanart'):
                    if addon.getSetting('use_thumb') == "true":
                        fanArt = thumbnail
                else:
                    fanArt = channel('fanart')[0].string
                if fanArt == None:
                    raise
            except:
                pass
            try:
                desc = channel('info')[0].string
                if desc == None:
                    raise
            except:
                desc = ''

            try:
                genre = channel('genre')[0].string
                if genre == None:
                    raise
            except:
                genre = ''

            try:
                date = channel('date')[0].string
                if date == None:
                    raise
            except:
                date = ''

            try:
                credits = channel('credits')[0].string
                if credits == None:
                    raise
            except:
                credits = ''

            try:
                addDir(name.encode('utf-8', 'ignore'),url.encode('utf-8'),3,thumbnail,fanArt,desc,genre,credits,date)
            except:
                addon_log('There was a problem adding directory - '+name.encode('utf-8', 'ignore'))
        getItems(items,fanArt)


def getSubChannelItems(name,url,fanart):
        soup = getSoup(url)
        channel_list = soup.find('subchannel', attrs={'name' : name.decode('utf-8')})
        items = channel_list('subitem')
        getItems(items,fanart)


def getItems(items,fanart):
        total = len(items)
        addon_log('Total Items: %s' %total)
        for item in items:
            #print item
            try:
                name = item('title')[0].string
                if name is None:
                    name = 'unknown?'
            except:
                addon_log('Name Error')
                name = ''


            try:
                if item('epg'):
                    if item.epg_url:
                        addon_log('Get EPG Regex')
                        epg_url = item.epg_url.string
                        epg_regex = item.epg_regex.string
                        epg_name = get_epg(epg_url, epg_regex)
                        if epg_name:
                            name += ' - ' + epg_name
                    elif item('epg')[0].string > 1:
                        name += getepg(item('epg')[0].string)
                else:
                    pass
            except:
                addon_log('EPG Error')
            try:
                url = []
                if len(item('link')) >0:
                    #print 'item link', item('link')
                    for i in item('link'):
                        if not i.string == None:
                            url.append(i.string)
                    
                elif len(item('sportsdevil')) >0:
                    for i in item('sportsdevil'):
                        if not i.string == None:
                            sportsdevil = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' +i.string
                            referer = item('referer')[0].string
                            if referer:
                                #print 'referer found'
                                sportsdevil = sportsdevil + '%26referer=' +referer
                            url.append(sportsdevil)
                elif len(item('p2p')) >0:
                    for i in item('p2p'):
                        if not i.string == None:
                            if 'sop://' in i:
                                sop = 'plugin://plugin.video.p2p-streams/?url='+i.string +'&amp;mode=2&amp;' + 'name='+name 
                                url.append(sop) 
                            else:
                                p2p='plugin://plugin.video.p2p-streams/?url='+i.string +'&amp;mode=1&amp;' + 'name='+name 
                                url.append(p2p)
                elif len(item('vaughn')) >0:
                    for i in item('vaughn'):
                        if not i.string == None:
                            vaughn = 'plugin://plugin.stream.vaughnlive.tv/?mode=PlayLiveStream&amp;channel='+i.string
                            url.append(vaughn)
                elif len(item('ilive')) >0:
                    for i in item('ilive'):
                        if not i.string == None:
                            if not 'http' in i.string:
                                ilive = 'plugin://plugin.video.tbh.ilive/?url=http://www.streamlive.to/view/'+i.string+'&amp;link=99&amp;mode=iLivePlay'
                            else:
                                ilive = 'plugin://plugin.video.tbh.ilive/?url='+i.string+'&amp;link=99&amp;mode=iLivePlay'
                elif len(item('yt-dl')) >0:
                    for i in item('yt-dl'):
                        if not i.string == None:
                            ytdl = i.string + '&mode=18'
                            url.append(ytdl)  
                if len(url) < 1:
                    raise
            except:
                addon_log('Error <link> element, Passing:'+name.encode('utf-8', 'ignore'))
                continue
                
            isXMLSource=False

            try:
                isXMLSource = item('externallink')[0].string
            except: pass
            
            if isXMLSource:
                url=[isXMLSource]
                isXMLSource=True
            else:
                isXMLSource=False
            
            try:
                thumbnail = item('thumbnail')[0].string
                if thumbnail == None:
                    raise
            except:
                thumbnail = ''
            try:
                if not item('fanart'):
                    if addon.getSetting('use_thumb') == "true":
                        fanArt = thumbnail
                    else:
                        fanArt = fanart
                else:
                    fanArt = item('fanart')[0].string
                if fanArt == None:
                    raise
            except:
                fanArt = fanart
            try:
                desc = item('info')[0].string
                if desc == None:
                    raise
            except:
                desc = ''

            try:
                genre = item('genre')[0].string
                if genre == None:
                    raise
            except:
                genre = ''

            try:
                date = item('date')[0].string
                if date == None:
                    raise
            except:
                date = ''

            regexs = None
            if item('regex'):
                try:
                    reg_item = item('regex')
                    regexs = parse_regex(reg_item)
                except:
                    pass            
           
            try:
                if len(url) > 1:
                    alt = 0
                    playlist = []
                    for i in url:
                        playlist.append(i)
                    if addon.getSetting('add_playlist') == "false":                    
                            for i in url:
                                alt += 1
                                addLink(i,'%s) %s' %(alt, name.encode('utf-8', 'ignore')),thumbnail,fanArt,desc,genre,date,True,playlist,regexs,total)                            
                    else:
                        addLink('', name.encode('utf-8', 'ignore'),thumbnail,fanArt,desc,genre,date,True,playlist,regexs,total)
                else:
                    if not isXMLSource:    
                        addLink(url[0],name.encode('utf-8', 'ignore'),thumbnail,fanArt,desc,genre,date,True,None,regexs,total)
                    else: 
                        addDir(name.encode('utf-8'),url[0].encode('utf-8'),1,thumbnail,fanart,desc,genre,date,None,'source')
                        
                    #print 'success'
            except:
                addon_log('There was a problem adding item - '+name.encode('utf-8', 'ignore'))
        

def parse_regex(reg_item):
                try:
                    regexs = {}
                    for i in reg_item:
                        regexs[i('name')[0].string] = {}
                        #regexs[i('name')[0].string]['expre'] = i('expres')[0].string
                        try:
                            regexs[i('name')[0].string]['expre'] = i('expres')[0].string
                            if not regexs[i('name')[0].string]['expre']:
                                regexs[i('name')[0].string]['expre']=''
                        except:
                            addon_log("Regex: -- No Referer --")
                        regexs[i('name')[0].string]['page'] = i('page')[0].string
                        try:
                            regexs[i('name')[0].string]['refer'] = i('referer')[0].string
                        except:
                            addon_log("Regex: -- No Referer --")
                        try:
                            regexs[i('name')[0].string]['connection'] = i('connection')[0].string
                        except:
                            addon_log("Regex: -- No connection --")
                        try:
                            regexs[i('name')[0].string]['origin'] = i('origin')[0].string
                        except:
                            addon_log("Regex: -- No origin --")
                        try:
                            regexs[i('name')[0].string]['includeheaders'] = i('includeheaders')[0].string
                        except:
                            addon_log("Regex: -- No includeheaders --")                            
                            
                        try:
                            regexs[i('name')[0].string]['x-req'] = i('x-req')[0].string
                        except:
                            addon_log("Regex: -- No x-req --")
                        try:
                            regexs[i('name')[0].string]['x-forward'] = i('x-forward')[0].string
                        except:
                            addon_log("Regex: -- No x-forward --")

                        try:
                            regexs[i('name')[0].string]['agent'] = i('agent')[0].string
                        except:
                            addon_log("Regex: -- No User Agent --")
                        try:
                            regexs[i('name')[0].string]['post'] = i('post')[0].string
                        except:
                            addon_log("Regex: -- Not a post")
                        try:
                            regexs[i('name')[0].string]['rawpost'] = i('rawpost')[0].string
                        except:
                            addon_log("Regex: -- Not a rawpost")
                        try:
                            regexs[i('name')[0].string]['htmlunescape'] = i('htmlunescape')[0].string
                        except:
                            addon_log("Regex: -- Not a htmlunescape")


                        try:
                            regexs[i('name')[0].string]['readcookieonly'] = i('readcookieonly')[0].string
                        except:
                            addon_log("Regex: -- Not a readCookieOnly")
                        #print i
                        try:
                            regexs[i('name')[0].string]['cookiejar'] = i('cookiejar')[0].string
                            if not regexs[i('name')[0].string]['cookiejar']:
                                regexs[i('name')[0].string]['cookiejar']=''
                        except:
                            addon_log("Regex: -- Not a cookieJar")							
                        try:
                            regexs[i('name')[0].string]['setcookie'] = i('setcookie')[0].string
                        except:
                            addon_log("Regex: -- Not a setcookie")
                        try:
                            regexs[i('name')[0].string]['appendcookie'] = i('appendcookie')[0].string
                        except:
                            addon_log("Regex: -- Not a appendcookie")
                                                    
                        try:
                            regexs[i('name')[0].string]['ignorecache'] = i('ignorecache')[0].string
                        except:
                            addon_log("Regex: -- no ignorecache")
                        #try:
                        #    regexs[i('name')[0].string]['ignorecache'] = i('ignorecache')[0].string
                        #except:
                        #    addon_log("Regex: -- no ignorecache")			

                    regexs = urllib.quote(repr(regexs))
                    return regexs
                    #print regexs
                except:
                    regexs = None
                    addon_log('regex Error: '+name.encode('utf-8', 'ignore'))
#copies from lamda's implementation
def get_ustream(url):
    try:
        for i in range(1, 51):
            result = getUrl(url)
            if "EXT-X-STREAM-INF" in result: return url
            if not "EXTM3U" in result: return
            xbmc.sleep(2000)
        return
    except:
        return
        
 
def getRegexParsed(regexs, url,cookieJar=None,forCookieJarOnly=False,recursiveCall=False,cachedPages={}, rawPost=False, cookie_jar_file=None):#0,1,2 = URL, regexOnly, CookieJarOnly
        if not recursiveCall:
            regexs = eval(urllib.unquote(regexs))
        #cachedPages = {}
        #print 'url',url
        doRegexs = re.compile('\$doregex\[([^\]]*)\]').findall(url)
        #print 'doRegexs',doRegexs,regexs
        setresolved=True
              
 


        for k in doRegexs:
            if k in regexs:
                #print 'processing ' ,k
                m = regexs[k]
                #print m
                cookieJarParam=False


                if  'cookiejar' in m: # so either create or reuse existing jar
                    #print 'cookiejar exists',m['cookiejar']
                    cookieJarParam=m['cookiejar']
                    if  '$doregex' in cookieJarParam:
                        cookieJar=getRegexParsed(regexs, m['cookiejar'],cookieJar,True, True,cachedPages)
                        cookieJarParam=True
                    else:
                        cookieJarParam=True
                #print 'm[cookiejar]',m['cookiejar'],cookieJar
                if cookieJarParam:
                    if cookieJar==None:
                        #print 'create cookie jar'
                        cookie_jar_file=None
                        if 'open[' in m['cookiejar']:
                            cookie_jar_file=m['cookiejar'].split('open[')[1].split(']')[0]
                            
                        cookieJar=getCookieJar(cookie_jar_file)
                        if cookie_jar_file:
                            saveCookieJar(cookieJar,cookie_jar_file)
                        #import cookielib
                        #cookieJar = cookielib.LWPCookieJar()
                        #print 'cookieJar new',cookieJar
                    elif 'save[' in m['cookiejar']:
                        cookie_jar_file=m['cookiejar'].split('save[')[1].split(']')[0]
                        complete_path=os.path.join(profile,cookie_jar_file)
                        print 'complete_path',complete_path
                        saveCookieJar(cookieJar,cookie_jar_file)
                        
 
                if  m['page'] and '$doregex' in m['page']:
                    m['page']=getRegexParsed(regexs, m['page'],cookieJar,recursiveCall=True,cachedPages=cachedPages)

                if 'setcookie' in m and m['setcookie'] and '$doregex' in m['setcookie']:
                    m['setcookie']=getRegexParsed(regexs, m['setcookie'],cookieJar,recursiveCall=True,cachedPages=cachedPages)
                if 'appendcookie' in m and m['appendcookie'] and '$doregex' in m['appendcookie']:
                    m['appendcookie']=getRegexParsed(regexs, m['appendcookie'],cookieJar,recursiveCall=True,cachedPages=cachedPages)

                 
                if  'post' in m and '$doregex' in m['post']:
                    m['post']=getRegexParsed(regexs, m['post'],cookieJar,recursiveCall=True,cachedPages=cachedPages)
                    print 'post is now',m['post']

                if  'rawpost' in m and '$doregex' in m['rawpost']:
                    m['rawpost']=getRegexParsed(regexs, m['rawpost'],cookieJar,recursiveCall=True,cachedPages=cachedPages,rawPost=True)
                    print 'rawpost is now',m['rawpost']
  
                if 'rawpost' in m and '$epoctime$' in m['rawpost']:
                    m['rawpost']=m['rawpost'].replace('$epoctime$',getEpocTime())
  
                if 'rawpost' in m and '$epoctime2$' in m['rawpost']:
                    m['rawpost']=m['rawpost'].replace('$epoctime2$',getEpocTime2())

  
                link=''
                if m['page'] and m['page'] in cachedPages and not 'ignorecache' in m and forCookieJarOnly==False :
                    link = cachedPages[m['page']]
                else:
                    if m['page'] and  not m['page']=='' and  m['page'].startswith('http'):
                        if '$epoctime$' in m['page']:
                            m['page']=m['page'].replace('$epoctime$',getEpocTime())
                        if '$epoctime2$' in m['page']:
                            m['page']=m['page'].replace('$epoctime2$',getEpocTime2())

                        #print 'Ingoring Cache',m['page']
                        page_split=m['page'].split('|')
                        pageUrl=page_split[0]
                        header_in_page=None
                        if len(page_split)>1:
                            header_in_page=page_split[1]
                        req = urllib2.Request(pageUrl)
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
                        if 'refer' in m:
                            req.add_header('Referer', m['refer'])
                        if 'agent' in m:
                            req.add_header('User-agent', m['agent'])
                        if 'x-req' in m:
                            req.add_header('X-Requested-With', m['x-req'])
                        if 'x-forward' in m:
                            req.add_header('X-Forwarded-For', m['x-forward'])
                        if 'setcookie' in m:
                            print 'adding cookie',m['setcookie']
                            req.add_header('Cookie', m['setcookie'])
                        if 'appendcookie' in m:
                            print 'appending cookie to cookiejar',m['appendcookie']
                            cookiestoApend=m['appendcookie']
                            cookiestoApend=cookiestoApend.split(';')
                            for h in cookiestoApend:
                                n,v=h.split('=')
                                w,n= n.split(':')
                                ck = cookielib.Cookie(version=0, name=n, value=v, port=None, port_specified=False, domain=w, domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
                                cookieJar.set_cookie(ck)

                                

                            
                        if 'origin' in m:
                            req.add_header('Origin', m['origin'])
                        if header_in_page:
                            header_in_page=header_in_page.split('&')
                            for h in header_in_page:
                                n,v=h.split('=')
                                req.add_header(n,v)


                        if not cookieJar==None:
                            #print 'cookieJarVal',cookieJar
                            cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
                            opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
                            opener = urllib2.install_opener(opener)
                        if 'connection' in m:
                            print '..........................connection//////.',m['connection']
                            from keepalive import HTTPHandler
                            keepalive_handler = HTTPHandler()
                            opener = urllib2.build_opener(keepalive_handler)
                            urllib2.install_opener(opener)
                            
                        #print 'after cookie jar'
                        post=None

                        if 'post' in m:
                            postData=m['post']
                            if '$LiveStreamRecaptcha' in postData:
                                (captcha_challenge,catpcha_word)=processRecaptcha(m['page'])
                                if captcha_challenge:
                                    postData+='recaptcha_challenge_field:'+captcha_challenge+',recaptcha_response_field:'+catpcha_word
                            splitpost=postData.split(',');
                            post={}
                            for p in splitpost:
                                n=p.split(':')[0];
                                v=p.split(':')[1];
                                post[n]=v
                            post = urllib.urlencode(post)

                        if 'rawpost' in m:
                            post=m['rawpost']
                            if '$LiveStreamRecaptcha' in post:
                                (captcha_challenge,catpcha_word)=processRecaptcha(m['page'])
                                if captcha_challenge:
                                   post+='&recaptcha_challenge_field='+captcha_challenge+'&recaptcha_response_field='+catpcha_word


                            

                        if post:
                            response = urllib2.urlopen(req,post)
                        else:
                            response = urllib2.urlopen(req)

                        link = response.read()
                        link=javascriptUnEscape(link)
                        if 'includeheaders' in m:
                            link+=str(response.headers.get('Set-Cookie'))

                        response.close()
                        cachedPages[m['page']] = link
                        #print link
                        print 'store link for',m['page'],forCookieJarOnly
                        
                        if forCookieJarOnly:
                            return cookieJar# do nothing
                    elif m['page'] and  not m['page'].startswith('http'):
                        if m['page'].startswith('$pyFunction:'):
                            val=doEval(m['page'].split('$pyFunction:')[1],'',cookieJar )
                            if forCookieJarOnly:
                                return cookieJar# do nothing
                            link=val
                        else:
                            link=m['page']
                if '$pyFunction:playmedia(' in m['expre'] or  any(x in url for x in g_ignoreSetResolved):
                    setresolved=False
                if  '$doregex' in m['expre']:
                    m['expre']=getRegexParsed(regexs, m['expre'],cookieJar,recursiveCall=True,cachedPages=cachedPages)
                    
                print 'exp k and url'
                print m['expre'],k,url
                print 'aa'
                
                if not m['expre']=='':
                    print 'doing it ',m['expre']
                    if '$LiveStreamCaptcha' in m['expre']:
                        val=askCaptcha(m,link,cookieJar)
                        print 'url and val',url,val
                        url = url.replace("$doregex[" + k + "]", val)
                    elif m['expre'].startswith('$pyFunction:'):

                        val=doEval(m['expre'].split('$pyFunction:')[1],link,cookieJar )

                        print 'url k val',url,k,val

                        url = url.replace("$doregex[" + k + "]", val)
                    else:
                        if not link=='':
                            reg = re.compile(m['expre']).search(link)
                            val=''
                            try:
                                val=reg.group(1).strip()
                            except: traceback.print_exc()
                        else:
                            val=m['expre']
                        if rawPost:
                            print 'rawpost'
                            val=urllib.quote_plus(val)
                        if 'htmlunescape' in m:
                            #val=urllib.unquote_plus(val)
                            import HTMLParser
                            val=HTMLParser.HTMLParser().unescape(val)                     
                        url = url.replace("$doregex[" + k + "]", val)
                        #return val
                else:           
                    url = url.replace("$doregex[" + k + "]",'')
        if '$epoctime$' in url:
            url=url.replace('$epoctime$',getEpocTime())
        if '$epoctime2$' in url:
            url=url.replace('$epoctime2$',getEpocTime2())

        if '$GUID$' in url:
            import uuid
            url=url.replace('$GUID$',str(uuid.uuid1()).upper())
        if '$get_cookies$' in url:
            url=url.replace('$get_cookies$',getCookiesString(cookieJar))   

        if recursiveCall: return url
        print 'final url',url
        item = xbmcgui.ListItem(path=url)
        
        if setresolved:
            print 'now doing set resolved',item
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
        else:
            xbmc.Player( xbmc.PLAYER_CORE_MPLAYER ).play(url)
            
        
def getmd5(t):
    import hashlib
    h=hashlib.md5()
    h.update(t)
    return h.hexdigest()

def decrypt_vaughnlive(encrypted):
    retVal=""
    for val in encrypted.split(':'):
        retVal+=chr(int(val.replace("0m0",""))/84/5)
    return retVal

def playmedia(media_url):
    try:
        import  CustomPlayer
        player = CustomPlayer.MyXBMCPlayer()
        listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ), path=media_url )
        player.play( media_url,listitem)
        xbmc.sleep(1000)
        while player.is_active:
            xbmc.sleep(200)
    except:
        traceback.print_exc()
    return ''
    
        
def get_saw_rtmp(page_value, referer=None):
    if referer:
        referer=[('Referer',referer)]
    if page_value.startswith("http"):
        page_url=page_value
        page_value= getUrl(page_value,headers=referer)

    str_pattern="(eval\(function\(p,a,c,k,e,d.*)"

    reg_res=re.compile(str_pattern).findall(page_value)
    r=""
    if reg_res and len(reg_res)>0:
        for v in reg_res:
            r1=get_unpacked(v)
            r2=re_me(r1,'\'(.*?)\'')
            if 'unescape' in r1:
                r1=urllib.unquote(r2)
            r+=r1+'\n'
        print 'final value is ',r
        
        page_url=re_me(r,'src="(.*?)"')
        
        page_value= getUrl(page_url,headers=referer)

    #print page_value

    rtmp=re_me(page_value,'streamer\'.*?\'(.*?)\'\)')
    playpath=re_me(page_value,'file\',\s\'(.*?)\'')

    
    return rtmp+' playpath='+playpath +' pageUrl='+page_url
    
def get_leton_rtmp(page_value, referer=None):
    if referer:
        referer=[('Referer',referer)]
    if page_value.startswith("http"):
        page_value= getUrl(page_value,headers=referer)
    str_pattern="var a = (.*?);\s*var b = (.*?);\s*var c = (.*?);\s*var d = (.*?);\s*var f = (.*?);\s*var v_part = '(.*?)';"
    reg_res=re.compile(str_pattern).findall(page_value)[0] 

    a,b,c,d,f,v=(reg_res)
    f=int(f)
    a=int(a)/f
    b=int(b)/f
    c=int(c)/f
    d=int(d)/f

    ret= 'rtmp://' + str(a) + '.' + str(b) + '.' + str(c) + '.' + str(d) + v;
    return ret


def SaveToFile(file_name,page_data,append=False):
    if append:
        f = open(file_name, 'a')
        f.write(page_data)
        f.close()        
    else:
        f=open(file_name,'wb')
        f.write(page_data)
        f.close()
        return ''
    
def LoadFile(file_name):
	f=open(file_name,'rb')
	d=f.read()
	f.close()
	return d
    
def get_packed_iphonetv_url(page_data):
	import re,base64,urllib; 
	s=page_data
	while '(atob(' in s: 
		s=re.compile('"(.*?)"').findall(s)[0]; 
		s=  base64.b64decode(s); 
		s=urllib.unquote(s); 
	print s
	return s


    
def get_dag_url(page_data):
    print 'get_dag_url',page_data
    if page_data.startswith('http://dag.total-stream.net'):
        headers=[('User-Agent','Verismo-BlackUI_(2.4.7.5.8.0.34)')]
        page_data=getUrl(page_data,headers=headers);

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


def get_unwise( str_eval):
    page_value=""
    try:        
        ss="w,i,s,e=("+str_eval+')' 
        exec (ss)
        page_value=unwise_func(w,i,s,e)
    except: traceback.print_exc(file=sys.stdout)
    #print 'unpacked',page_value
    return page_value
    
def unwise_func( w, i, s, e):
    lIll = 0;
    ll1I = 0;
    Il1l = 0;
    ll1l = [];
    l1lI = [];
    while True:
        if (lIll < 5):
            l1lI.append(w[lIll])
        elif (lIll < len(w)):
            ll1l.append(w[lIll]);
        lIll+=1;
        if (ll1I < 5):
            l1lI.append(i[ll1I])
        elif (ll1I < len(i)):
            ll1l.append(i[ll1I])
        ll1I+=1;
        if (Il1l < 5):
            l1lI.append(s[Il1l])
        elif (Il1l < len(s)):
            ll1l.append(s[Il1l]);
        Il1l+=1;
        if (len(w) + len(i) + len(s) + len(e) == len(ll1l) + len(l1lI) + len(e)):
            break;
        
    lI1l = ''.join(ll1l)#.join('');
    I1lI = ''.join(l1lI)#.join('');
    ll1I = 0;
    l1ll = [];
    for lIll in range(0,len(ll1l),2):
        #print 'array i',lIll,len(ll1l)
        ll11 = -1;
        if ( ord(I1lI[ll1I]) % 2):
            ll11 = 1;
        #print 'val is ', lI1l[lIll: lIll+2]
        l1ll.append(chr(    int(lI1l[lIll: lIll+2], 36) - ll11));
        ll1I+=1;
        if (ll1I >= len(l1lI)):
            ll1I = 0;
    ret=''.join(l1ll)
    if 'eval(function(w,i,s,e)' in ret:
        print 'STILL GOing'
        ret=re.compile('eval\(function\(w,i,s,e\).*}\((.*?)\)').findall(ret)[0] 
        return get_unwise(ret)
    else:
        print 'FINISHED'
        return ret
    
def get_unpacked( page_value, regex_for_text='', iterations=1, total_iteration=1):
    try:        
        reg_data=None
        if page_value.startswith("http"):
            page_value= getUrl(page_value)
        print 'page_value',page_value
        if regex_for_text and len(regex_for_text)>0:
            page_value=re.compile(regex_for_text).findall(page_value)[0] #get the js variable
        
        page_value=unpack(page_value,iterations,total_iteration)
    except: traceback.print_exc(file=sys.stdout)
    print 'unpacked',page_value
    if 'sav1live.tv' in page_value:
        page_value=page_value.replace('sav1live.tv','sawlive.tv') #quick fix some bug somewhere
        print 'sav1 unpacked',page_value
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

def __unpack(p, a, c, k, e, d, iteration,v=1):

    #with open('before file'+str(iteration)+'.js', "wb") as filewriter:
    #    filewriter.write(str(p))
    while (c >= 1):
        c = c -1
        if (k[c]):
            aa=str(__itoaNew(c, a))
            if v==1:
                p=re.sub('\\b' + aa +'\\b', k[c], p)# THIS IS Bloody slow!
            else:
                p=findAndReplaceWord(p,aa,k[c])

            #p=findAndReplaceWord(p,aa,k[c])

            
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
    #print 'cookieString',cookieString
    return cookieString


def saveCookieJar(cookieJar,COOKIEFILE):
	try:
		complete_path=os.path.join(profile,COOKIEFILE)
		cookieJar.save(complete_path,ignore_discard=True)
	except: pass

def getCookieJar(COOKIEFILE):

	cookieJar=None
	if COOKIEFILE:
		try:
			complete_path=os.path.join(profile,COOKIEFILE)
			cookieJar = cookielib.LWPCookieJar()
			cookieJar.load(complete_path,ignore_discard=True)
		except: 
			cookieJar=None
	
	if not cookieJar:
		cookieJar = cookielib.LWPCookieJar()
	
	return cookieJar
    
def doEval(fun_call,page_data,Cookie_Jar):
    ret_val=''
    if functions_dir not in sys.path:
        sys.path.append(functions_dir)
    
    print fun_call
    try:
        py_file='import '+fun_call.split('.')[0]
        print py_file,sys.path
        exec( py_file)
        print 'done'
    except:
        print 'error in import'
        traceback.print_exc(file=sys.stdout)
    print 'ret_val='+fun_call
    exec ('ret_val='+fun_call)
    print ret_val
    #exec('ret_val=1+1')
    return str(ret_val)
    
def processRecaptcha(url):
	html_text=getUrl(url)
	recapChallenge=""
	solution=""
	cap_reg="<script.*?src=\"(.*?recap.*?)\""
	match =re.findall(cap_reg, html_text)
	captcha=False
	captcha_reload_response_chall=None
	solution=None
	
	if match and len(match)>0: #new shiny captcha!
		captcha_url=match[0]
		captcha=True
		
		cap_chall_reg='challenge.*?\'(.*?)\''
		cap_image_reg='\'(.*?)\''
		captcha_script=getUrl(captcha_url)
		recapChallenge=re.findall(cap_chall_reg, captcha_script)[0]
		captcha_reload='http://www.google.com/recaptcha/api/reload?c=';
		captcha_k=captcha_url.split('k=')[1]
		captcha_reload+=recapChallenge+'&k='+captcha_k+'&captcha_k=1&type=image&lang=en-GB'
		captcha_reload_js=getUrl(captcha_reload)
		captcha_reload_response_chall=re.findall(cap_image_reg, captcha_reload_js)[0]
		captcha_image_url='http://www.google.com/recaptcha/api/image?c='+captcha_reload_response_chall
		if not captcha_image_url.startswith("http"):
			captcha_image_url='http://www.google.com/recaptcha/api/'+captcha_image_url
		import random
		n=random.randrange(100,1000,5)
		local_captcha = os.path.join(profile,str(n) +"captcha.img" )
		localFile = open(local_captcha, "wb")
		localFile.write(getUrl(captcha_image_url))
		localFile.close()
		solver = InputWindow(captcha=local_captcha)
		solution = solver.get()
		os.remove(local_captcha)
	return captcha_reload_response_chall ,solution

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

def get_decode(str,reg=None):
	if reg:
		str=re.findall(reg, str)[0]
	s1 = urllib.unquote(str[0: len(str)-1]);
	t = '';
	for i in range( len(s1)):
		t += chr(ord(s1[i]) - s1[len(s1)-1]);
	t=urllib.unquote(t)
	print t
	return t

def javascriptUnEscape(str):
	js=re.findall('unescape\(\'(.*?)\'',str)
	print 'js',js
	if (not js==None) and len(js)>0:
		for j in js:
			#print urllib.unquote(j)
			str=str.replace(j ,urllib.unquote(j))
	return str

iid=0
def askCaptcha(m,html_page, cookieJar):
    global iid
    iid+=1
    expre= m['expre']
    page_url = m['page']
    captcha_regex=re.compile('\$LiveStreamCaptcha\[([^\]]*)\]').findall(expre)[0]

    captcha_url=re.compile(captcha_regex).findall(html_page)[0]
    print expre,captcha_regex,captcha_url
    if not captcha_url.startswith("http"):
        page_='http://'+"".join(page_url.split('/')[2:3])
        if captcha_url.startswith("/"):
            captcha_url=page_+captcha_url
        else:
            captcha_url=page_+'/'+captcha_url
    
    local_captcha = os.path.join(profile, str(iid)+"captcha.jpg" )
    localFile = open(local_captcha, "wb")
    print ' c capurl',captcha_url
    req = urllib2.Request(captcha_url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
    if 'refer' in m:
        req.add_header('Referer', m['refer'])
    if 'agent' in m:
        req.add_header('User-agent', m['agent'])
    if 'setcookie' in m:
        print 'adding cookie',m['setcookie']
        req.add_header('Cookie', m['setcookie'])
        
    #cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
    #opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    #opener = urllib2.install_opener(opener)
    urllib2.urlopen(req)
    response = urllib2.urlopen(req)

    localFile.write(response.read())
    response.close()
    localFile.close()
    solver = InputWindow(captcha=local_captcha)
    solution = solver.get()
    return solution
    
class InputWindow(xbmcgui.WindowDialog):
    def __init__(self, *args, **kwargs):
        self.cptloc = kwargs.get('captcha')
        self.img = xbmcgui.ControlImage(335,30,624,60,self.cptloc)
        self.addControl(self.img)
        self.kbd = xbmc.Keyboard()

    def get(self):
        self.show()
        time.sleep(2)        
        self.kbd.doModal()
        if (self.kbd.isConfirmed()):
            text = self.kbd.getText()
            self.close()
            return text
        self.close()
        return False
    
def getEpocTime():
    import time
    return str(int(time.time()*1000))

def getEpocTime2():
    import time
    return str(int(time.time()))

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


def getFavorites():
        items = json.loads(open(favorites).read())
        total = len(items)
        for i in items:
            name = i[0]
            url = i[1]
            iconimage = i[2]
            try:
                fanArt = i[3]
                if fanArt == None:
                    raise
            except:
                if addon.getSetting('use_thumb') == "true":
                    fanArt = iconimage
                else:
                    fanArt = fanart
            try: playlist = i[5]
            except: playlist = None
            try: regexs = i[6]
            except: regexs = None

            if i[4] == 0:
                addLink(url,name,iconimage,fanArt,'','','','fav',playlist,regexs,total)
            else:
                addDir(name,url,i[4],iconimage,fanart,'','','','','fav')


def addFavorite(name,url,iconimage,fanart,mode,playlist=None,regexs=None):
        favList = []
        try:
            # seems that after 
            name = name.encode('utf-8', 'ignore')
        except:
            pass
        if os.path.exists(favorites)==False:
            addon_log('Making Favorites File')
            favList.append((name,url,iconimage,fanart,mode,playlist,regexs))
            a = open(favorites, "w")
            a.write(json.dumps(favList))
            a.close()
        else:
            addon_log('Appending Favorites')
            a = open(favorites).read()
            data = json.loads(a)
            data.append((name,url,iconimage,fanart,mode))
            b = open(favorites, "w")
            b.write(json.dumps(data))
            b.close()


def rmFavorite(name):
        data = json.loads(open(favorites).read())
        for index in range(len(data)):
            if data[index][0]==name:
                del data[index]
                b = open(favorites, "w")
                b.write(json.dumps(data))
                b.close()
                break
        xbmc.executebuiltin("XBMC.Container.Refresh")


def play_playlist(name, list):
        playlist = xbmc.PlayList(1)
        playlist.clear()
        item = 0
        for i in list:
            item += 1
            info = xbmcgui.ListItem('%s) %s' %(str(item),name))
            playlist.add(i, info)
        xbmc.executebuiltin('playlist.playoffset(video,0)')


def download_file(name, url):
        if addon.getSetting('save_location') == "":
            xbmc.executebuiltin("XBMC.Notification('LiveStreamsPro','Choose a location to save files.',15000,"+icon+")")
            addon.openSettings()
        params = {'url': url, 'download_path': addon.getSetting('save_location')}
        downloader.download(name, params)
        dialog = xbmcgui.Dialog()
        ret = dialog.yesno('LiveStreamsPro', 'Do you want to add this file as a source?')
        if ret:
            addSource(os.path.join(addon.getSetting('save_location'), name))


def addDir(name,url,mode,iconimage,fanart,description,genre,date,credits,showcontext=False):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
        ok=True
        if date == '':
            date = None
        else:
            description += '\n\nDate: %s' %date
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description, "Genre": genre, "dateadded": date, "credits": credits })
        liz.setProperty("Fanart_Image", fanart)
        if showcontext:
            contextMenu = []
            if showcontext == 'source':
                if name in str(SOURCES):
                    contextMenu.append(('Remove from Sources','XBMC.RunPlugin(%s?mode=8&name=%s)' %(sys.argv[0], urllib.quote_plus(name))))
            elif showcontext == 'download':
                contextMenu.append(('Download','XBMC.RunPlugin(%s?url=%s&mode=9&name=%s)'
                                    %(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))
            elif showcontext == 'fav':
                contextMenu.append(('Remove from LiveStreamsPro Favorites','XBMC.RunPlugin(%s?mode=6&name=%s)'
                                    %(sys.argv[0], urllib.quote_plus(name))))
            if not name in FAV:
                contextMenu.append(('Add to LiveStreamsPro Favorites','XBMC.RunPlugin(%s?mode=5&name=%s&url=%s&iconimage=%s&fanart=%s&fav_mode=%s)'
                         %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(fanart), mode)))
            liz.addContextMenuItems(contextMenu)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
def ytdl_download(url,title,media_type='video'):
    # play in xbmc while playing go back to contextMenu(c) to "!!Download!!"
    # Trial yasceen: seperate |User-Agent=
    import youtubedl
    if not url == '':
        if media_type== 'audio':
            youtubedl.single_YD(url,download=True,audio=True)
        else:
            youtubedl.single_YD(url,download=True)   
    elif xbmc.Player().isPlaying() == True :
        import YDStreamExtractor
        if YDStreamExtractor.isDownloading() == True:
            #print 'already downloading Add to que'
            YDStreamExtractor.manageDownloads()
        else:
            xbmc_url = xbmc.Player().getPlayingFile()
            print 'title is ',title
            xbmc_url = xbmc_url.split('|User-Agent=')[0]
            info = {'url':xbmc_url,'title':title,'media_type':media_type}
            youtubedl.single_YD('',download=True,dl_info=info)    
    else:
        xbmc.executebuiltin("XBMC.Notification(DOWNLOAD,First Play [COLOR yellow]WHILE playing download[/COLOR] ,10000)")
 
def search(site_name,search_term=None):
    thumbnail=''
    if os.path.exists(history) == False or addon.getSetting('clearseachhistory')=='true':
        SaveToFile(history,'')
        addon.setSetting("clearseachhistory","false")
    if site_name == 'history' :
        content = LoadFile(history)
        match = re.compile('(.+?):(.*?)(?:\r|\n)').findall(content)
        print len(match)
        for name,search_term in match:
            if 'plugin://' in search_term:
                addLink(search_term, name,thumbnail,'','','','','',None,'',total=int(len(match)))
            else:
                addDir(name+':'+search_term,name,26,icon,FANART,'','','','')
    if not search_term:    
        keyboard = xbmc.Keyboard('','Enter Search Term')
        keyboard.doModal()
        if (keyboard.isConfirmed() == False):
            return
        search_term = keyboard.getText()
        if len(search_term) == 0:
            return        
    search_term = search_term.replace(' ','+')
    search_term = search_term.encode('utf-8')
    if 'youtube' in site_name:
        #youtube = youtube#Lana Del Rey
        import _ytplist
        print 'search_termsearch_term',search_term
        search_res = {}
        #search_res={'item69': {'date': '2015-01-12T16:32:09.000Z', 'url': 'whDJofPk9xQ', 'desc': '', 'title': 'Adele Playing With Her Vanity'}, 'item68': {'date': '2015-01-12T16:45:46.000Z', 'url': 'afZLd5fM3Hw', 'desc': '', 'title': 'Set fire to the rain   Adele Cover by 12 years old Jannina W   YouTube 2'}, 'item65': {'date': '2015-01-12T17:47:27.000Z', 'url': 'HbMbJC1hj_o', 'desc': 'This is my version of Make You Feel My Love. Please subscribe and leave me a comment. :)  I used this karaoke acoustic version for my cover : https://www.youtube.com/watch?v=JFwd16raBKU...', 'title': 'Make You Feel My Love - Adele (Covered by Verena)'}, 'item64': {'date': '2015-01-12T17:52:26.000Z', 'url': 'PyCgXAdgnTU', 'desc': 'The delaney version ', 'title': 'Adele "someone like you"'}, 'item67': {'date': '2015-01-12T16:46:47.000Z', 'url': 'dYM3ilsr1zU', 'desc': '', 'title': 'Someone like you   Adele Cover by 12 years old Jannina W   YouTube'}, 'item66': {'date': '2015-01-12T17:35:50.000Z', 'url': 'aIWBYGoGjgQ', 'desc': '', 'title': 'Adele Jumping On Her Trampoline'}, 'item61': {'date': '2015-01-12T19:14:58.000Z', 'url': 'OLa7QVrnya8', 'desc': "Sorry for some background noises. It's just for fun, but advice is always welcome! :) Please subscribe Background music credits: TheKARAOKEChannel Instagram: Alysamijn.", 'title': 'Adele - Lovesong (Cover by Alysamijn)'}, 'item60': {'date': '2015-01-12T19:24:25.000Z', 'url': '7fAARN-oIOs', 'desc': 'Please Subscribe and give this video a Thumbs Up! Leave a comment in the section below: What song do you want me to sing next?!', 'title': 'Cover- Adele Someone Like You'}, 'item63': {'date': '2015-01-12T18:22:29.000Z', 'url': 'hp-k-aRD_oY', 'desc': '', 'title': "Adele ABC's"}, 'item62': {'date': '2015-01-12T19:10:15.000Z', 'url': '9Ka2gZJS0nM', 'desc': 'My nieces wants to sing with adele!! They want to show the best they got ( thumbs up please) girls got dreams make it happen!', 'title': 'Children version of adele'}, 'item58': {'date': '2015-01-12T19:44:12.000Z', 'url': '9iqp5JYAYWE', 'desc': 'Here is my cover of the soundtrack from the movie James Bond 007 - Skyfall. I hope you enjoy!', 'title': "Adele - Skyfall (Nicole's cover) with lyrics"}, 'item59': {'date': '2015-01-12T19:35:15.000Z', 'url': '0gcfKumwKqk', 'desc': 'Me singing Make you feel my Love in the style of Adele Hope you like it ;) Please subscribe :)', 'title': 'Make you feel my Love - Adele - Cover - Lea Knauer'}, 'item50': {'date': '2015-01-12T20:39:59.000Z', 'url': 'AkUucURHPqg', 'desc': "Not showing my face because I am shy... It's good or bad don't care this is my first time", 'title': 'Cover of Adele-someone like you my fav song'}, 'item51': {'date': '2015-01-12T20:38:10.000Z', 'url': '0B-rGDMvVpI', 'desc': 'Ignore the terrible picture quality!! (All rights reserved to artist)', 'title': 'To make you feel my love cover (Adele)'}, 'item52': {'date': '2015-01-12T20:25:29.000Z', 'url': 'XkgnNxI19Ec', 'desc': 'Adele ponytail hairstyle with bump Medium long hair tutorial Coiffure facile a faire cheveux mi long hair tutorial for medium hair, ponytail hairstyles, hairstyles with extensions, how to,...', 'title': 'Adele ponytail hairstyle with bump Medium long hair tutorial Coiffure facile a faire cheveux mi long'}, 'item53': {'date': '2015-01-12T20:14:31.000Z', 'url': 'zfiw3tWcuaQ', 'desc': 'http://www.gohotels.com/en-location/sainte-adele-ca.htm.', 'title': 'Hotel Mont-Gabriel, Sainte-Adele, Quebec, Canada'}, 'item54': {'date': '2015-01-12T20:11:34.000Z', 'url': 'NT-EqVycoYA', 'desc': 'please leave thoughts !! thank you so much.', 'title': 'rolling in the deep Adele cover'}, 'item55': {'date': '2015-01-12T20:10:42.000Z', 'url': '0VQcLJ9XsCk', 'desc': 'Ein Ausschnitt von Rolling in the Deep von Adele. Ich hoffe euch gefllt es. Ich mchte mich fr Textfehler usw. entschuldigen.', 'title': 'A pice of -Rolling in the Deep from Adele '}, 'item56': {'date': '2015-01-12T20:02:18.000Z', 'url': 'eTbDUG7Mmt0', 'desc': "Fantastic cover of the well known Adele song by my picture perfect student, Samantha, who's so awesome at being expressive with this powerful tune. Samantha's guitar playing is good also:...", 'title': 'SOMEONE LIKE YOU - Adele (cover by Samantha)'}, 'item57': {'date': '2015-01-12T19:54:02.000Z', 'url': 'bUrXHjPqdT8', 'desc': 'https://salikc.wordpress.com/wp-admin/customize.php.', 'title': 'ADELE   Skyfall'}, 'item8': {'date': '2015-01-13T04:01:16.000Z', 'url': 'PaoZicH0v40', 'desc': 'Titulo : Set Fire To The Rain . Artista: Adele .', 'title': 'Adele Set Fire To The Rain'}, 'item9': {'date': '2015-01-13T03:57:54.000Z', 'url': 'bPDdOtBqCO0', 'desc': 'Xoxoxo, Instagram/Twitter/SoundCloud: @TheRoZMusic. Song-Writer. Recording Artist. Rapper. Dancer. Actor. Model. 15.', 'title': 'Love Me Harder and Rolling In the Deep -Ariana Grande/Adele- Cover by Ro-Z'}, 'item2': {'date': '2015-01-13T05:40:24.000Z', 'url': 'DeO5lhANhd8', 'desc': 'What did you know about Adele? This video will tell you some facts about Adele: 1.Her ful name is adele Laurie Blue adkins 2.she is fan of spice girl 3.she learn music since she was 4 4.She...', 'title': '5 Fact About ADELE'}, 'item3': {'date': '2015-01-13T05:29:31.000Z', 'url': 'CA8MdUzd17k', 'desc': 'Masih belum diketahui kapan Adele akan merilis album barunya. Setelah sebelumnya dikabarkan menggandeng seorang produser musik pop Greg Kurstin, kini salah seorang produser lainnya Paul ...', 'title': 'Album Baru Adele Semakin Tak Jelas Kapan Rilisnya'}, 'item6': {'date': '2015-01-13T04:16:52.000Z', 'url': 'LGlQMgs6TDU', 'desc': "Today it's not a dubstep, but rather a remix of Adele's set fire to the rain. This remix includes live vocals, violin cover, as well as a piano cover as well. It took alot of hard work, so...", 'title': 'Adele Set Fire to the Rain Remix'}, 'item7': {'date': '2015-01-13T04:12:57.000Z', 'url': '237lTKyuJXw', 'desc': 'GernaeAdeleShow @COCO_LOUIE @truthORdarion Live from Washington, DC every Saturday 10am www.ListenVisionLive.com.', 'title': 'Gernae Adele Show 1/10-1'}, 'item4': {'date': '2015-01-13T05:17:26.000Z', 'url': 'knKgKX9Pph0', 'desc': 'Trinity singing Rolling in the Deep by Adele for her middle school American idol finals competition.', 'title': 'Trinity singing Rolling in the Deep by Adele'}, 'item5': {'date': '2015-01-13T04:58:53.000Z', 'url': '2kU0lRLKbgc', 'desc': 'Malia Bortnem sings at the annual Hawley High School Variety Show.', 'title': 'Make you feel my love - Adele - Malia Bortnem'}, 'item47': {'date': '2015-01-12T21:11:41.000Z', 'url': 'BqjLLBqcHsI', 'desc': 'A clean version of Hometown Glory by Adele. I do not own this song, just this edit. Picture belongs to Adele I took out words around 2:47 You can download this using http://www.youtube-mp3.org.', 'title': 'Hometown Glory- Adele (Clean Radio Edit)'}, 'item46': {'date': '2015-01-12T21:21:05.000Z', 'url': 'TRXXzhMRSxA', 'desc': 'ISCRIVITI AL CANALE PER RIMANERE AGGIORNATO!!! "Set fire to the rain" originally by Adele Arrangment by: https://www.youtube.com/watch?v=i8rfa0qwEj4 Attori: Angelica Braccio & Vittorio Salvo...', 'title': 'Set fire to the rain - Adele (cover) Enrica Cataldi'}, 'item45': {'date': '2015-01-12T21:34:22.000Z', 'url': 'qENfxoUxdnA', 'desc': '', 'title': "Adele Producer Paul Epworth Says Her Long Awaited Follow Up 'Will Come When It's Ready'"}, 'item44': {'date': '2015-01-12T21:36:47.000Z', 'url': 'EX_01sbBZcA', 'desc': '', 'title': 'Adele make you feel my love ( cover )'}, 'item43': {'date': '2015-01-12T21:42:59.000Z', 'url': 'nCqu_aMieXw', 'desc': '', 'title': 'Conligus Elite Star Webinar (Italian) at (12/01/2015) with Adele Lumia & Massimo Del Moro'}, 'item42': {'date': '2015-01-12T21:53:23.000Z', 'url': 'Y80m120iR_M', 'desc': 'Este vdeo es sobre CLASE CON MARIO SEGUNDA PARTE.', 'title': 'Clase con Mario / Segunda Parte - Adele - Set Fire to the Rain by Ren Olivera Lahera'}, 'item41': {'date': '2015-01-12T22:16:06.000Z', 'url': 'on9z3MAjKUg', 'desc': 'Adele is such a great singer!! Enjoy my verizon. Xoxo :))', 'title': 'Adele- Rolling in the Deep. (Cover by Victoria Bitler)'}, 'item40': {'date': '2015-01-12T22:15:35.000Z', 'url': 'pyZ217fM278', 'desc': 'my own take on turning tables...by adele.', 'title': 'adele turning tables'}, 'item49': {'date': '2015-01-12T20:39:17.000Z', 'url': 'Y9-ks2nH6V0', 'desc': '', 'title': 'Conligus Elite Star Webinar (French) at (12/01/2015) with Adele Lumia'}, 'item48': {'date': '2015-01-12T20:41:50.000Z', 'url': '0RLPVOCFZ1c', 'desc': 'Mandisa Delves, in our Customer Relations Department singing Adele\'s "Rolling in the Deep" today! Isn\'t she amazing? The beginning of Michael + Son IDOL!', 'title': 'Mandisa Delves performing Adele\'s "Rolling in the Deep"'}, 'item32': {'date': '2015-01-12T23:35:51.000Z', 'url': 'Pe35ioaXg1I', 'desc': 'via YouTube Capture.', 'title': 'Someone Like You - Adele'}, 'item33': {'date': '2015-01-12T23:31:08.000Z', 'url': 'YLVxbAROsCc', 'desc': "Brooklyn Brooks plays piano while singing 'Someone Like You' an Adele song.", 'title': 'Brooklyn Brooks singing "Adele - Someone Like You\'.'}, 'item30': {'date': '2015-01-12T23:47:22.000Z', 'url': 'jBhfYjT5nOw', 'desc': '', 'title': 'Adele - Rolling in the Deep cover acustico'}, 'item31': {'date': '2015-01-12T23:40:58.000Z', 'url': 'rQuirdr2tRI', 'desc': 'Coreografia e performance: Natlia Fernandes Msica: Adele - Hometown Glory.', 'title': 'Adele - Hometown Glory | Coreografia contempornea por Natlia Fernandes'}, 'item36': {'date': '2015-01-12T22:44:04.000Z', 'url': 'MeeCQwj3fv4', 'desc': 'Oh Katie.', 'title': 'Someone Like You - Adele (Cover)'}, 'item37': {'date': '2015-01-12T22:33:44.000Z', 'url': '3fte1sVRnCU', 'desc': '', 'title': "Adele Producer Paul Epworth Says Her Long Awaited Follow Up 'Will Come When It's Ready'"}, 'item34': {'date': '2015-01-12T23:02:28.000Z', 'url': 'nZFIYWQn-RE', 'desc': 'This video is for my momma #2! She loves when i sing this at karaoke & asked me to make a video. Hope you enjoy! Instagram- @heeeybrookiee_.', 'title': 'Adele- Make you feel my love Cover by Brooke Garvin (:'}, 'item35': {'date': '2015-01-12T22:51:38.000Z', 'url': '2ngnqbygpyM', 'desc': 'Tiny Piano is the easiest piano on the App Store. Download for free: http://bit.ly/tinypiano.', 'title': 'Someone Like You - Adele - Tiny Piano'}, 'item38': {'date': '2015-01-12T22:31:58.000Z', 'url': '06qYMiTP25M', 'desc': '', 'title': "Adele Producer Paul Epworth Says Her Long Awaited Follow Up 'Will Come When It's Ready'"}, 'item39': {'date': '2015-01-12T22:27:05.000Z', 'url': '6JDS_wwq0o0', 'desc': "I don't own anything I had a cold but I hoped you enjoyed!", 'title': 'Cover of Turning tables by Adele'}, 'item94': {'date': '2014-12-17T23:10:33.000Z', 'url': 'Gstz7jyzHbk', 'desc': 'I love the lyrics and melody of this piece. The original version was written by Bob Dylan and many people have covered it but my favourite rendition of it is...', 'title': 'Adele - Make You Feel My Love  - Cover by Katey'}, 'item95': {'date': '2014-12-15T15:00:12.000Z', 'url': 'xpzs1ky4h_Q', 'desc': "Before taking over the music charts with hit after hit, Jessie J and Adele were classmates at the UK's BRIT School. Jessie J shares school memories, and prai...", 'title': 'Jessie J & Adele Go Wayyy Back'}, 'item96': {'date': '2014-12-11T09:35:08.000Z', 'url': 'Sx5-04fHsMg', 'desc': "Hi, I'm Stephanie Valentin (website : http://www.stval.fr), a french artist : violinist, singer, composer, painter and sculptor. SUBSCRIBE to my channel : ht...", 'title': 'Adele - Rolling in the deep - Trumpet-Violin Cover by Stephanie Valentin'}, 'item97': {'date': '2014-12-07T13:22:12.000Z', 'url': 'xci2QG-w5BI', 'desc': 'Ben Haenow Alex Haenow Adel one and only cover living room sessions @Bhaenow @Alexxx335.', 'title': 'Adele One And Only'}, 'item90': {'date': '2014-12-26T23:13:35.000Z', 'url': 'OLSBcBc4njs', 'desc': 'n finala X Factor Romnia, sezonul patru, Alexandra Crian a cntat melodia interpretat de Adele - "Someone Like You".', 'title': 'Duel: Adele - "Someone Like You". Interpretarea Alexandrei Crian, la X Factor!'}, 'item91': {'date': '2014-12-24T19:03:21.000Z', 'url': 'GlwMTQFLHdU', 'desc': 'Get "A Very Postmodern Christmas": http://msclvr.co/7jYj5B PMJ Tix: http://tickets.turnupgroup.com/postmodernjukebox Check out the amazing Robyn Adele Anders...', 'title': 'My Favorite Things - Jazz Cover ft. Robyn Adele Anderson'}, 'item92': {'date': '2014-12-20T07:05:36.000Z', 'url': 'k6pUqzwaEnk', 'desc': 'Adele Buon Onomastico"24 Dicembre San Adele"Tantissimi Auguri Adele"Merry Christmas Happy new year" Adele Buon Onomastico"24 Dicembre San Adele"Tantissimi Au...', 'title': 'Adele Buon Onomastico"24 Dicembre San Adele"Tantissimi Auguri Adele"Merry Christmas Happy new year"'}, 'item93': {'date': '2014-12-18T16:16:41.000Z', 'url': 'FfgVyRfNKLs', 'desc': 'Sper Sbado Sensacional es el programa de variedades con mayor raiting de la televisin venezolana. Con casi 40 aos al aire, este gran magazine ha sufrido ...', 'title': 'Sper Sbado Sensacional - Buscando una Estrella - Vanessa Querales como Adele'}, 'item98': {'date': '2014-12-02T22:49:38.000Z', 'url': 'eD6iuXmOCGs', 'desc': 'Get our Christmas album on sale now: http://msclvr.co/E1SfgV PMJ Europe Tix: http://tickets.turnupgroup.com/postmo... The holiday season is officially here, ...', 'title': 'Hark! The Herald Angels We Have Heard On High - PMJ ft. Robyn Adele Anderson & Dave Koz'}, 'item99': {'date': '2014-12-02T15:54:43.000Z', 'url': 'ax7zpGpo0Mg', 'desc': 'Alexandra Crisan interpreteaza One and Only - Adele la duel X Factor Romania 2014.', 'title': 'Alexandra Crisan - One and Only (Adele) - X Factor'}, 'item21': {'date': '2015-01-13T01:43:43.000Z', 'url': 's2OKm0wyo4o', 'desc': '', 'title': 'I found a boy(cover-Adele)-Gii Tr New'}, 'item20': {'date': '2015-01-13T01:45:51.000Z', 'url': '4Jpd0kCDxgc', 'desc': "50 Cent Adele's vevo 2014 Turning Tables.", 'title': "Copy of 50 Cent Adele's vevo 2014 Turning Tables"}, 'item23': {'date': '2015-01-13T01:15:42.000Z', 'url': 'BEk1Yk_64DE', 'desc': '', 'title': 'Me singing adele'}, 'item22': {'date': '2015-01-13T01:31:37.000Z', 'url': 'SGPKjMorPQk', 'desc': 'Enjoy! (Sorry, the keyboard is a little dinky.)', 'title': '"Someone Like You" (Adele) cover'}, 'item25': {'date': '2015-01-13T00:46:31.000Z', 'url': 'm0e-YbE5DcY', 'desc': "I know, I sucked. It's ok & I'm sorry its only 30 seconds long.", 'title': 'Rolling in the deep by adele!'}, 'item24': {'date': '2015-01-13T01:04:38.000Z', 'url': '3M_oxRwSF_g', 'desc': '', 'title': 'Kendall dancing to turning table by Adele'}, 'item27': {'date': '2015-01-13T00:21:50.000Z', 'url': 'meoSaZ5gIBs', 'desc': 'facebook.com/adambombu @adambombyout I will see youz guyz later.', 'title': 'Someone Like You Adele - Cover'}, 'item26': {'date': '2015-01-13T00:44:53.000Z', 'url': 'LPVUWODr_78', 'desc': '', 'title': 'Copy of Someone like you ! adele Cover'}, 'item29': {'date': '2015-01-13T00:08:38.000Z', 'url': 'Vf1BGPSIufc', 'desc': 'Hope you enjoyed it leave any comments below thanks for watching :)', 'title': 'Adele someone like you'}, 'item28': {'date': '2015-01-13T00:19:03.000Z', 'url': '0Z6YWprNJ2g', 'desc': "The Sibling Rivalry's first gig at Cusina Lounge in Toronto December 28, 2014 Guitar - Jazz Wayde Violin - Julien Waynes Percussion - Jean Wesley.", 'title': 'Rolling in the Deep - Adele Cover'}, 'item83': {'date': '2015-01-12T05:06:38.000Z', 'url': 'NHNlS0lwWEo', 'desc': '', 'title': 'IJK - The Cyber Academy Covers - Adele - Turning Tables'}, 'item82': {'date': '2015-01-12T05:24:23.000Z', 'url': 'VvEYhuDlkII', 'desc': 'Copyright Disclaimer Under Section 107 of the Copyright Act 1976, allowance is made for "fair use" for purposes such as criticism, comment, news reporting, teaching, scholarship, and research....', 'title': 'Dimitri Vangelis & Wyman vs Adele - Set ID2 To The Rain (Danilo  Mashup)'}, 'item81': {'date': '2015-01-12T06:58:50.000Z', 'url': 'Z9bGFHfJBoI', 'desc': '', 'title': 'adele 4'}, 'item80': {'date': '2015-01-12T06:58:50.000Z', 'url': 'FxSe51ksd9U', 'desc': '', 'title': 'adele 5 1'}, 'item87': {'date': '2015-01-11T22:36:05.000Z', 'url': 'PhPdKY3-FwI', 'desc': '', 'title': 'Adele - Turning Tables (Cover)'}, 'item86': {'date': '2015-01-11T23:51:09.000Z', 'url': 'IgU2F3XmX6k', 'desc': 'it sounds better in person.', 'title': 'some one like u by-Adele sang by saydee ponciroli'}, 'item85': {'date': '2015-01-12T01:22:01.000Z', 'url': 'moPjuPWZA4U', 'desc': '', 'title': 'Rolling in the Deep~ Adele'}, 'item84': {'date': '2015-01-12T02:42:19.000Z', 'url': 'y9HaBXIa8xE', 'desc': '', 'title': 'skyfall adele live'}, 'item89': {'date': '2014-12-30T18:41:53.000Z', 'url': '0PEeH6R60jM', 'desc': 'Subscribe to XXL: http://bit.ly/subscribe-xxl Trae talks to XXL about working with Adele. Available for the first time on the official XXL YouTube channel. G...', 'title': 'Trae On Working With Adele (June 2011)'}, 'item88': {'date': '2015-01-11T19:38:52.000Z', 'url': 'prRt8GyBacM', 'desc': 'Description.', 'title': 'ASL song Someone to Love by Adele'}, 'item101': {'date': '2014-11-29T20:22:24.000Z', 'url': 'fnCDKJPqfmM', 'desc': 'Adele - Daydreamer (Traduo)', 'title': 'Adele - Daydreamer (Traduo)'}, 'item100': {'date': '2014-11-29T20:43:02.000Z', 'url': 'mdk0V3CIyUA', 'desc': 'n bootcamp-ul din sezonul 4 de la "X Factor", Alexandra Crian a cntat melodia interpretat de Adele - "One And Only".', 'title': 'Duel: Adele - "One And Only". Interpretarea Alexandrei Crian, la X Factor!'}, 'item18': {'date': '2015-01-13T01:57:39.000Z', 'url': '5BxeGLRwHrI', 'desc': 'http://www.youtube.com/upload)', 'title': 'Adele - Someone Like You'}, 'item19': {'date': '2015-01-13T01:45:40.000Z', 'url': 'PvW88KWwdlo', 'desc': 'Adle (Adle Exarchopoulos) tiene quince aos y sabe que lo normal es salir con chicos, pero tiene dudas sobre su sexualidad. Una noche conoce y se enamora inesperadamente de Emma (La...', 'title': "La vie d' Adel - La vida de Adele / Audio Espaol"}, 'item14': {'date': '2015-01-13T02:49:46.000Z', 'url': 'KNABK2qjsP4', 'desc': 'Another cover:) hope u like it I apologize for any lagginess bartleediddlydoo@gmail.com Emilyshafermusic@gmail.com Www.instagram.com/emilyshafer22 Dont forget to comment and subscribe! BTW:: ...', 'title': 'Rolling in the deep (cover) by adele'}, 'item15': {'date': '2015-01-13T02:16:45.000Z', 'url': 'rU8W6Cz8g54', 'desc': '', 'title': 'Skyfall (Adele) -- Cover at Minnesota YMCA Youth In Government Talent Show'}, 'item16': {'date': '2015-01-13T02:01:23.000Z', 'url': 'BjHWA6_Puj8', 'desc': 'PDF tab: http://goo.gl/Egya6M.', 'title': '(Adele) Make you feel my love -  guitar Tab  Sungha Jung'}, 'item17': {'date': '2015-01-13T02:00:06.000Z', 'url': 'Gjbe7A7DGQQ', 'desc': "50 Cent Adele's vevo 2014 music audio.", 'title': "Copy of 50 Cent Adele's vevo 2014 music audio"}, 'item10': {'date': '2015-01-13T03:56:42.000Z', 'url': 'Q7If4qEUFKo', 'desc': '', 'title': 'Someone Like You- Adele (cover)'}, 'item11': {'date': '2015-01-13T03:47:13.000Z', 'url': 'GwB6_rgs1FU', 'desc': 'Adele du Rand shares her insights on why it is important for employees to have a moment to pause during demanding and busy work schedules. In this video, Mowana Spa introduces their mobile...', 'title': 'Adele du Rand & Mowana Spa 2015 01 08'}, 'item12': {'date': '2015-01-13T03:45:04.000Z', 'url': '9IeJR5jcxXw', 'desc': "Adele - Someone Like You Adele - Someone Like You (DeeJay Sunlight) Thalia - Un Alma Sentenciada Kylie Minogue - Timebomb Kylie Minogue - Timebomb (Dada Remix) 2ne1 - I'm The Best.", 'title': 'Adele ft  Thalia, 2NE1, & Kylie Minogue - Someone Like Un Alma Sentenciada Mashup'}, 'item13': {'date': '2015-01-13T03:09:50.000Z', 'url': 'bdHyTdnwTHg', 'desc': "This is my cover of Adele's beautiful Make You Feel My Love. Hope you enjoy. Subscribe for future videos!", 'title': 'Make You Feel My Love - Michaela Curtis- Adele Cov'}, 'item78': {'date': '2015-01-12T15:00:48.000Z', 'url': '4btbatrUQJo', 'desc': '', 'title': "Don't you remember- adele"}, 'item79': {'date': '2015-01-12T14:29:56.000Z', 'url': 'XAp1MzMv7zI', 'desc': 'Synthesia Piano Tutorial [COVER] More on: Facebook: http://www.facebook.com/SynthesiaMaster Tags: synthesia, synthesia piano, synthesia song, synthesia piano tutorial.', 'title': 'Adele - Skyfall - Synthesia Piano Tutorial [COVER]'}, 'item76': {'date': '2015-01-12T15:37:15.000Z', 'url': 'uVtxb8Lvb_w', 'desc': 'tambah nganggur z.', 'title': 'ada saja kreasinya nyanyi adele someone like U'}, 'item77': {'date': '2015-01-12T15:04:36.000Z', 'url': 'ZKLZQVauePE', 'desc': '', 'title': 'Pour Adele'}, 'item74': {'date': '2015-01-12T15:38:28.000Z', 'url': 'kb8A9-YhoD8', 'desc': "it was very Stormy outside and we didn't have anything to do, so we decided why not Record & Shoot a short music video... the song is dedicated to our son Andre... Filmed, Edited & Mixed...", 'title': "'Love Song' - (Olla's Cover of Adele's Cover)"}, 'item75': {'date': '2015-01-12T15:36:50.000Z', 'url': 'HUhGP_kuo70', 'desc': '', 'title': 'Skyfall   Adele Cover by 12 years old Jannina W'}, 'item72': {'date': '2015-01-12T16:05:07.000Z', 'url': 'myiSD_YLxTU', 'desc': '', 'title': 'I found a boy - Adele Cover'}, 'item73': {'date': '2015-01-12T15:50:23.000Z', 'url': 'xqSAko5wLoE', 'desc': 'Adele Set Fire To The Rain Coverversion by Angela Brand www.tonstudio-hillstation.de.', 'title': 'Adele - Set Fire To The Rain - Cover by Angela Brand'}, 'item70': {'date': '2015-01-12T16:25:03.000Z', 'url': 'LjrWWz146No', 'desc': '', 'title': 'Hometown Glory- Adele- Piano/Voix'}, 'item71': {'date': '2015-01-12T16:10:37.000Z', 'url': '1CJDM-BDbhk', 'desc': '', 'title': "Adele - Don't you remember"}}
        search_res = _ytplist.YoUTube('searchYT',youtube=search_term,max_page=4,nosave='nosave')
        #print search_res
        total = len(search_res)
        print 'total search_res::', str(total)
        for item in search_res:
            #print search_res[item]['title']
            try:
                name = search_res[item]['title']
                date= search_res[item]['date']
                try:
                    description = search_res[item]['desc']
                except Exception:
                    description = 'UNAVAIABLE'

                url = 'plugin://plugin.video.youtube/play/?video_id=' + search_res[item]['url']
                #print url
                thumbnail ='http://img.youtube.com/vi/'+search_res[item]['url']+'/0.jpg'
                addLink(url, name,thumbnail,'','','','','',None,'',total)
            except Exception:
                print 'ignore this linkddddddddddd'
        page_data = site_name +':'+ search_term + '\n'
        SaveToFile(os.path.join(profile,'history'),page_data,append=True)
    elif 'dmotion' in site_name:
        urlMain = "https://api.dailymotion.com" 
        #youtube = youtube#Lana Del Rey
        import _DMsearch
        familyFilter = str(addon.getSetting('familyFilter'))
        _DMsearch.listVideos(urlMain+"/videos?fields=description,duration,id,owner.username,taken_time,thumbnail_large_url,title,views_total&search="+search_term+"&sort=relevance&limit=100&family_filter="+familyFilter+"&localization=en_EN&page=1")
    
        page_data = site_name +':'+ search_term+ '\n'
        SaveToFile(os.path.join(profile,'history'),page_data,append=True)        
    elif 'PulsarM' in site_name:
        urlMain = "https://api.dailymotion.com" 
        keyboard = xbmc.Keyboard('','Enter Search Term')
        keyboard.doModal()
        if (keyboard.isConfirmed() == False):
            return
        search_term = keyboard.getText()
        if len(search_term) == 0:
            return        
        search_term = search_term.replace(' ','+')
        url= 'plugin://plugin.video.pulsar/search?q='+search_term
        print url
        
    elif 'IMDBidplay' in site_name:
        urlMain = "http://www.omdbapi.com/?t=" 
        url= urlMain+search_term
        print url
        headers = dict({'User-Agent':'Mozilla/5.0 (Windows NT 6.3; rv:33.0) Gecko/20100101 Firefox/33.0','Referer': 'http://joker.org/','Accept-Encoding':'gzip, deflate','Content-Type': 'application/json;charset=utf-8','Accept': 'application/json, text/plain, */*'})
    
        r=requests.get(url,headers=headers)
        data = r.json()
        res = data['Response']
        if res == 'True':
            imdbID = data['imdbID']
            name= data['Title'] + data['Released']
            dialog = xbmcgui.Dialog()
            ret = dialog.yesno('Check Movie Title', 'PLAY :: %s ?'%name)
            if ret:
                url = 'plugin://plugin.video.pulsar/movie/'+imdbID+'/play'
                page_data = name +':'+ url+ '\n'
                SaveToFile(history,page_data,append=True)
                return url
        else:
            xbmc.executebuiltin("XBMC.Notification(LiveStreamsPro,No IMDB match found ,7000,"+icon+")")
    


def addLink(url,name,iconimage,fanart,description,genre,date,showcontext,playlist,regexs,total,setCookie=""):
        #print 'url,name',url,name
        contextMenu =[]
        try:
            name = name.encode('utf-8')
        except: pass
        ok = True
        if regexs: 
            mode = '17'
            contextMenu.append(('[COLOR white]!!Download Currently Playing!![/COLOR]','XBMC.RunPlugin(%s?url=%s&mode=21&name=%s)'
                                    %(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))           
        elif  any(x in url for x in resolve_url) and  url.startswith('http'):
            mode = '19'
            contextMenu.append(('[COLOR white]!!Download Currently Playing!![/COLOR]','XBMC.RunPlugin(%s?url=%s&mode=21&name=%s)'
                                    %(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))           
        elif url.endswith('&mode=18'):
            url=url.replace('&mode=18','')
            mode = '18' 
            contextMenu.append(('[COLOR white]!!Download!![/COLOR]','XBMC.RunPlugin(%s?url=%s&mode=23&name=%s)'
                                    %(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))           
            
        else: 
            mode = '12'
            contextMenu.append(('[COLOR white]!!Download Currently Playing!![/COLOR]','XBMC.RunPlugin(%s?url=%s&mode=21&name=%s)'
                                    %(sys.argv[0], urllib.quote_plus(url), urllib.quote_plus(name))))           
        u=sys.argv[0]+"?"
        play_list = False
        if playlist:
            if addon.getSetting('add_playlist') == "false":
                u += "url="+urllib.quote_plus(url)+"&mode="+mode
            else:
                u += "mode=13&name=%s&playlist=%s" %(urllib.quote_plus(name), urllib.quote_plus(str(playlist).replace(',','|')))
                play_list = True
        else:
            u += "url="+urllib.quote_plus(url)+"&mode="+mode
        if regexs:
            u += "&regexs="+regexs
        if not setCookie == '':
            u += "&setCookie="+urllib.quote_plus(setCookie)
  
        if date == '':
            date = None
        else:
            description += '\n\nDate: %s' %date
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description, "Genre": genre, "dateadded": date })
        liz.setProperty("Fanart_Image", fanart)
        if (not play_list) and not any(x in url for x in g_ignoreSetResolved):#  (not url.startswith('plugin://plugin.video.f4mTester')):
            if regexs:
                if '$pyFunction:playmedia(' not in urllib.unquote_plus(regexs):
                    #print 'setting isplayable',url, urllib.unquote_plus(regexs)
                    liz.setProperty('IsPlayable', 'true')
            else:
                liz.setProperty('IsPlayable', 'true')
        else:
            addon_log( 'NOT setting isplayable'+url)
        if showcontext:
            contextMenu = []
            if showcontext == 'fav':
                contextMenu.append(
                    ('Remove from LiveStreamsPro Favorites','XBMC.RunPlugin(%s?mode=6&name=%s)'
                     %(sys.argv[0], urllib.quote_plus(name)))
                     )
            elif not name in FAV:
                fav_params = (
                    '%s?mode=5&name=%s&url=%s&iconimage=%s&fanart=%s&fav_mode=0'
                    %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(fanart))
                    )
                if playlist:
                    fav_params += 'playlist='+urllib.quote_plus(str(playlist).replace(',','|'))
                if regexs:
                    fav_params += "&regexs="+regexs
                contextMenu.append(('Add to LiveStreamsPro Favorites','XBMC.RunPlugin(%s)' %fav_params))
            liz.addContextMenuItems(contextMenu)
        if not playlist is None:
            if addon.getSetting('add_playlist') == "false":
                playlist_name = name.split(') ')[1]
                contextMenu_ = [
                    ('Play '+playlist_name+' PlayList','XBMC.RunPlugin(%s?mode=13&name=%s&playlist=%s)'
                     %(sys.argv[0], urllib.quote_plus(playlist_name), urllib.quote_plus(str(playlist).replace(',','|'))))
                     ]
                liz.addContextMenuItems(contextMenu_)
        #print 'adding',name
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,totalItems=total)
        #print 'added',name
        return ok
def playsetresolved(url,name,iconimage):
    liz = xbmcgui.ListItem(name, iconImage=iconimage)
    liz.setInfo(type='Video', infoLabels={'Title':name})
    liz.setProperty("IsPlayable","true")
    liz.setPath(url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)


## Thanks to daschacka, an epg scraper for http://i.teleboy.ch/programm/station_select.php
##  http://forum.xbmc.org/post.php?p=936228&postcount=1076
def getepg(link):
        url=urllib.urlopen(link)
        source=url.read()
        url.close()
        source2 = source.split("Jetzt")
        source3 = source2[1].split('programm/detail.php?const_id=')
        sourceuhrzeit = source3[1].split('<br /><a href="/')
        nowtime = sourceuhrzeit[0][40:len(sourceuhrzeit[0])]
        sourcetitle = source3[2].split("</a></p></div>")
        nowtitle = sourcetitle[0][17:len(sourcetitle[0])]
        nowtitle = nowtitle.encode('utf-8')
        return "  - "+nowtitle+" - "+nowtime


def get_epg(url, regex):
        data = makeRequest(url)
        try:
            item = re.findall(regex, data)[0]
            return item
        except:
            addon_log('regex failed')
            addon_log(regex)
            return


xbmcplugin.setContent(int(sys.argv[1]), 'movies')

try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)
except:
    pass
try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
except:
    pass
try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_DATE)
except:
    pass
try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_GENRE)
except:
    pass

params=get_params()

url=None
name=None
mode=None
playlist=None
iconimage=None
fanart=FANART
playlist=None
fav_mode=None
regexs=None

try:
    url=urllib.unquote_plus(params["url"]).decode('utf-8')
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    iconimage=urllib.unquote_plus(params["iconimage"])
except:
    pass
try:
    fanart=urllib.unquote_plus(params["fanart"])
except:
    pass
try:
    mode=int(params["mode"])
except:
    pass
try:
    playlist=eval(urllib.unquote_plus(params["playlist"]).replace('|',','))
except:
    pass
try:
    fav_mode=int(params["fav_mode"])
except:
    pass
try:
    regexs=params["regexs"]
except:
    pass

addon_log("Mode: "+str(mode))
if not url is None:
    addon_log("URL: "+str(url.encode('utf-8')))
addon_log("Name: "+str(name))

if mode==None:
    addon_log("getSources")
    getSources()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==1:
    addon_log("getData")
    getData(url,fanart)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==2:
    addon_log("getChannelItems")
    getChannelItems(name,url,fanart)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==3:
    addon_log("getSubChannelItems")
    getSubChannelItems(name,url,fanart)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==4:
    addon_log("getFavorites")
    getFavorites()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==5:
    addon_log("addFavorite")
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    addFavorite(name,url,iconimage,fanart,fav_mode)

elif mode==6:
    addon_log("rmFavorite")
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    rmFavorite(name)

elif mode==7:
    addon_log("addSource")
    addSource(url)

elif mode==8:
    addon_log("rmSource")
    rmSource(name)

elif mode==9:
    addon_log("download_file")
    download_file(name, url)

elif mode==10:
    addon_log("getCommunitySources")
    getCommunitySources()

elif mode==11:
    addon_log("addSource")
    addSource(url)

elif mode==12:
    addon_log("setResolvedUrl")

    if not any(x in url for x in g_ignoreSetResolved):#not url.startswith("plugin://plugin.video.f4mTester") :
        item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
        #xbmc.playlist(xbmc.playlist_video).clear()
        #xbmc.playlist(xbmc.playlist_video).add(url)
        #xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(item=url)
    else:
        print 'Not setting setResolvedUrl'
        xbmc.executebuiltin('XBMC.RunPlugin('+url+')')


elif mode==13:
    addon_log("play_playlist")
    play_playlist(name, playlist)

elif mode==14:
    addon_log("get_xml_database")
    get_xml_database(url)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==15:
    addon_log("browse_xml_database")
    get_xml_database(url, True)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==16:
    addon_log("browse_community")
    getCommunitySources(True)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

elif mode==17:
    addon_log("getRegexParsed")
    getRegexParsed(regexs, url)
elif mode==18:
    addon_log("youtubedl")
    try:
        import youtubedl
    except Exception:
        xbmc.executebuiltin("XBMC.Notification(LiveStreamsPro,Please [COLOR yellow]install Youtube-dl[/COLOR] module ,10000,"")")
        
    print url
    stream_url=youtubedl.single_YD(url)
    playsetresolved(stream_url,name,iconimage)
    #item = xbmcgui.ListItem(path=stream_url)
    #xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)    
elif mode==19:
    addon_log("Commonresolvers")
    import commonresolvers
    resolved=commonresolvers.get(url)
    if resolved:
        if isinstance(resolved,list):
            for k in resolved:
                quality = addon.getSetting('quality')
                if k['quality'] == 'HD'  :
                    resolver = k['url']
                    break
                elif k['quality'] == 'SD' :
                    resolver = k['url']        
                elif k['quality'] == '1080p' and addon.getSetting('1080pquality') == 'true' :
                    resolver = k['url']
                    break
        else:
            resolver = resolved        
        playsetresolved(resolver,name,iconimage)
    else: 
        print 'Probably,this host is not supported or resolver is broken::',url     

elif mode==21:
    addon_log("download current file using youtube-dl service")
    ytdl_download('',name,'video')
elif mode==23:
    addon_log("get info then download")
    ytdl_download(url,name,'video') 
elif mode==24:
    addon_log("Audio only youtube download")
    ytdl_download(url,name,'audio')
elif mode==25:
    addon_log("YouTube/DMotion")
    search(url)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==26:
    addon_log("YouTube/DMotion From Search History")
    name = name.split(':')
    search(url,search_term=name[1])
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==27:
    addon_log("Using IMDB id to play in Pulsar")
    pulsarIMDB=search(url)
    #playsetresolved(pulsarIMDB,name,iconimage)
    xbmc.Player().play(pulsarIMDB) 