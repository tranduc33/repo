# -*- coding: UTF-8 -*-
#---------------------------------------------------------------------
# File:    tvvn.py
# Version: 0.1.0
# Modified By: Son Tranduc
# Original Author: Binh Nguyen
#---------------------------------------------------------------------
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#---------------------------------------------------------------------

import os, re, sys, gzip, urllib, urllib2, string, xbmcaddon, xbmcplugin, xbmcgui, xbmcvfs
import requests
from resources.common_variables import *
from resources.scrape import *
from StringIO import StringIO
from cookielib import CookieJar

try:
        import json
except:
        import simplejson as json

addon = xbmcaddon.Addon('plugin.video.kenhtrongnuoc')
mysettings = xbmcaddon.Addon(id='plugin.video.kenhtrongnuoc')
profile = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile')).decode('utf-8')
home = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path')).decode('utf-8')
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
datafile = xbmc.translatePath(os.path.join(home, 'data.json'))

data = json.loads(open(datafile,"r").read())

jsonPath = xbmc.translatePath(os.path.join("special://home/addons/plugin.video.kenhtrongnuoc/resources", ""))

mode=None

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

params=get_params()

try:         chn=urllib.unquote_plus(params["chn"])
except: pass
try:         src=urllib.unquote_plus(params["src"])
except: pass
try:         mode=int(params["mode"])
except: pass

def construct_menu(namex):
        name = data['directories'][namex]['title']
        lmode = '2'
        iconimage = ''
        desc = data['directories'][namex]['desc']

        menu_items = data['directories'][namex]['content']
        for menu_item in menu_items:
                #type == channel
                if (menu_item['type'] == "chn"):
                        add_chn_link (menu_item['id'])
                #type == directory
                if (menu_item['type'] == "dir"):
                        add_dir_link (menu_item['id'])
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        return

def add_chn_link (namex):
        ok = True
        title = data['channels'][namex]['title']
        name = title
        iconimage = data['channels'][namex]['logo']
        desc = data['channels'][namex]['desc']
        #ref = data['channels'][namex]['src']['referer']
        stream_name = data['channels'][namex]['src']['playpath']
        src = data['channels'][namex]['src']['id']

        if (iconimage == ''):
                iconimage = 'default.png'
        if (mysettings.getSetting('descriptions')=='true' and desc != ''):
                if mysettings.getSetting('descriptions_on_right') == 'false':
                        name = desc+"    "+name
                else:
                        name = name+"    "+desc

        give_url = sys.argv[0]+"?mode=1&chn="+namex+"&src="+src
        liz = xbmcgui.ListItem(name)
        liz.setInfo(type="video", infoLabels={"title": name, "mediatype": "video"})
        liz.setArt({
           "icon": xbmc.translatePath(os.path.join(home, 'resources', 'logos', iconimage)),
           "thumb": xbmc.translatePath(os.path.join(home, 'resources', 'logos', iconimage)),
           "fanart": fanart
           })
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=give_url,listitem=liz)

def add_dir_link (namex):
        name = '['+data['directories'][namex]['title']+']'
        desc = data['directories'][namex]['desc']
        iconimage = data['directories'][namex]['logo']
        if (iconimage == ''):
                iconimage = 'default.png'
        if (mysettings.getSetting('descriptions')=='true' and desc != ''):
                if mysettings.getSetting('descriptions_on_right') == 'false':
                        name = desc+"    "+name
                else:
                        name = name+"    "+desc
        li = xbmcgui.ListItem(name)
        li.setInfo(type="video", infoLabels={"title": name, "mediatype": "video"})
        li.setArt({
           "icon": xbmc.translatePath(os.path.join(home, 'resources', 'logos', iconimage)),
           "thumb": xbmc.translatePath(os.path.join(home, 'resources', 'logos', iconimage)),
           "fanart": fanart
           })
        give_url = sys.argv[0]+"?mode=2&chn="+namex
        return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=give_url, listitem=li, isFolder=True)


def play_link(chn, src):
        item = xbmcgui.ListItem(chn)
        d_progress = xbmcgui.DialogProgress()
        d_progress.create("Please wait ...", addon.getLocalizedString(30009))
        cj = CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

        #m3u8 url from tvnet
        if data['channels'][chn]['src']['playpath'] == "m3u8_tvnet":
            # url = 'https://vtvgo.vn/xem-truc-tuyen-kenh-vtv1-1.html'
            # result = parse_url(url)
            url = 'http://au.tvnet.gov.vn/kenh-truyen-hinh/'+data['channels'][chn]['src']['page_id']
            stringA = opener.open(url).read().decode('utf-8')
            stringB = 'data-file="'
            stringC = '"'
            url = re.search(stringB+"(.*?)"+re.escape(stringC),stringA).group(1)
            
            stringA = opener.open(url).read().decode('utf-8')
            stringB = '"url": "'
            stringC = '"'
            full_url_BC = re.search(stringB+"(.*?)"+re.escape(stringC),stringA).group(1)
            full_url = full_url_BC


        #parse vtvgo
        if data['channels'][chn]['src']['playpath'] == "m3u8_vtvgo":
            url = data['channels'][chn]['src']['page_url']
            full_url = parse_vtvgo(url)

        #parse http://tvzz.101vn.com/
        if data['channels'][chn]['src']['playpath'] == "online":
            url = data['channels'][chn]['src']['page_url']
            full_url = parse_101vn(url)

        #parse https://now.vtc.vn/
        if data['channels'][chn]['src']['playpath'] == "vtc":
			full_url = data['channels'][chn]['src']['page_url']

        #parse vchannel
        if data['channels'][chn]['src']['playpath'] == "vchannel":
            url = data['channels'][chn]['src']['page_url']
            full_url = parse_vchannel(url)

        d_progress.close()

        #dialog = xbmcgui.Dialog()
        #dialog.textviewer('Plot',full_url )

        ok = xbmc.Player().play(full_url)


        return

KEY = get_key()

if  (str(KEY) == ""):
	macid = get_mac()
	dialog = xbmcgui.Dialog()
	dialog.textviewer("Warning!", "Unauthorized Device, Your MAC id:  "+macid)
	sys.exit()


def Init():
        construct_menu("root")
        # if (mysettings.getSetting('json_url_auto_update')=='true' and mysettings.getSetting('json_url')!=''):
        #         update_chn_list()

if mode==None:
        Init()
elif mode==1:
        play_link(chn, src)
elif mode==2:
        construct_menu(chn)
