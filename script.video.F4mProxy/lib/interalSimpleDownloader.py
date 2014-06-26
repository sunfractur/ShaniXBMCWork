
import xml.etree.ElementTree as etree
import base64
from struct import unpack, pack
import sys
import io
import os
import time
import itertools
import xbmcaddon
import xbmc
import urllib2,urllib
import traceback
import urlparse
import posixpath
import re
import socket

addon_id = 'script.video.F4mProxy'
selfAddon = xbmcaddon.Addon(id=addon_id)
__addonname__   = selfAddon.getAddonInfo('name')
__icon__        = selfAddon.getAddonInfo('icon')
downloadPath   = xbmc.translatePath(selfAddon.getAddonInfo('profile'))#selfAddon["profile"])
#F4Mversion=''

class interalSimpleDownloader():
   
    outputfile =''
    clientHeader=None
    def __init__(self):
        self.init_done=False
    def thisme(self):
        return 'aaaa'
   
    def openUrl(self,url, ischunkDownloading=False):
        try:
            post=None
            openner = urllib2.build_opener(urllib2.HTTPHandler, urllib2.HTTPSHandler)

            if post:
                req = urllib2.Request(url, post)
            else:
                req = urllib2.Request(url)
            
            ua_header=False
            if self.clientHeader:
                for n,v in self.clientHeader:
                    req.add_header(n,v)
                    if n=='User-Agent':
                        ua_header=True

            if not ua_header:
                req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
            #response = urllib2.urlopen(req)
            if self.proxy and (  (not ischunkDownloading) or self.use_proxy_for_chunks ):
                req.set_proxy(self.proxy, 'http')
            response = openner.open(req)

            return response
        except:
            print 'Error in getUrl'
            traceback.print_exc()
        return None

    def getUrl(self,url, ischunkDownloading=False):
        try:
            post=None
            openner = urllib2.build_opener(urllib2.HTTPHandler, urllib2.HTTPSHandler)

            if post:
                req = urllib2.Request(url, post)
            else:
                req = urllib2.Request(url)
            
            ua_header=False
            if self.clientHeader:
                for n,v in self.clientHeader:
                    req.add_header(n,v)
                    if n=='User-Agent':
                        ua_header=True

            if not ua_header:
                req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
            #response = urllib2.urlopen(req)
            if self.proxy and (  (not ischunkDownloading) or self.use_proxy_for_chunks ):
                req.set_proxy(self.proxy, 'http')
            response = openner.open(req)
            data=response.read()

            return data

        except:
            print 'Error in getUrl'
            traceback.print_exc()
        return None
            
    def myunit(self, out_stream, url, proxy=None,g_stopEvent=None):
        try:
            self.init_done=False
            self.init_url=url
            self.clientHeader=None
            self.status='init'
            self.proxy = proxy
            if self.proxy and len(self.proxy)==0:
                self.proxy=None
            self.out_stream=out_stream
            self.g_stopEvent=g_stopEvent
            if '|' in url:
                sp = url.split('|')
                url = sp[0]
                self.clientHeader = sp[1]
                self.clientHeader= urlparse.parse_qsl(self.clientHeader)
                
            print 'header recieved now url and headers are',url, self.clientHeader 
            self.status='init done'
            self.url=url
            #self.downloadInternal(  url)
            return True
            
            #os.remove(self.outputfile)
        except: 
            traceback.print_exc()
            self.status='finished'
        return False
     
        
    def keep_sending_video(self,dest_stream, segmentToStart=None, totalSegmentToSend=0):
        try:
            self.status='download Starting'
            self.downloadInternal(self.url,dest_stream)
        except: 
            traceback.print_exc()
        self.status='finished'
            
    def downloadInternal(self,url,dest_stream):
        try:
            url=self.url
            fileout=dest_stream
            self.status='bootstrap done'

            while True:
                    

                response=self.openUrl(url)
                buf="start"
                try:
                    while (buf != None and len(buf) > 0):
                        if self.g_stopEvent and self.g_stopEvent.isSet():
                            return
                        buf = response.read(200 * 1024)
                        fileout.write(buf)
                        #print 'writing something..............'
                        fileout.flush()                        
                    response.close()
                    fileout.close()
                    print time.asctime(), "Closing connection"
                except socket.error, e:
                    print time.asctime(), "Client Closed the connection."
                    try:
                        response.close()
                        fileout.close()
                    except Exception, e:
                        return
                except Exception, e:
                    traceback.print_exc(file=sys.stdout)
                    response.close()
                    fileout.close()
                

        except:
            traceback.print_exc()
            return