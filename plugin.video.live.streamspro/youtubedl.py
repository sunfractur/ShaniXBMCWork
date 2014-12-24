# -*- coding: utf-8 -*-
import xbmc,xbmcgui
try:
    from YDStreamExtractor import getVideoInfo
except Exception:
    print 'importing Error. You need youtubedl module which is in official xbmc.org'
    xbmc.executebuiltin("XBMC.Notification(LiveStreamsPro,Please [COLOR yellow]install Youtube-dl[/COLOR] module ,10000,"")")
    
def single_YD(page_data):
    info = getVideoInfo(page_data,quality=2,resolve_redirects=True)
    if info is None:
        print 'Fail to extract'
        return None    
    
    else:
        for s in info.streams():
            try:
                stream_url = s['xbmc_url'].encode('utf-8','ignore')
                return stream_url
            except Exception:
                return None             
