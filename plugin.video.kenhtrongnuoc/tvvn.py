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

#data = json.loads(open(datafile,"r").read())

jsonPath = xbmc.translatePath(os.path.join("special://home/addons/plugin.video.kenhtrongnuoc/resources", ""))

# request json at tdsolu
data = get_key()

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
        path = data['channels'][chn]['src']['playpath']
        link = data['channels'][chn]['src']['page_url']
        item = xbmcgui.ListItem(chn)
        d_progress = xbmcgui.DialogProgress()
        d_progress.create("Please wait ...", addon.getLocalizedString(30009))
        #cj = CookieJar()
        #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

        #parse tvnet
        if path == "m3u8_tvnet":
                full_url = checkOffLine(parse_tvnet(link))

        #parse vtvgo
        elif path == "m3u8_vtvgo":
                #url = data['channels'][chn]['src']['page_url']
                full_url = parse_vtvgo(link)
                #import web_pdb; web_pdb.set_trace()

        #parse https://now.vtc.vn/
        elif (path == "vtc") or (path == "m3u8"):
                link = data['channels'][chn]['src']['page_url']
                full_url = checkOffLine(link)

        #parse vchannel
        elif path == "vchannel":
                full_url = checkOffLine(parse_vchannel(link))

        #parse vcab7
        elif path == "vcab7":
                full_url = checkOffLine(parse_vcab7(link))

        #parse hplus
        elif path == "hplus":
                full_url = checkOffLine(parse_hplus(link))

        #parse non-scape channels
        elif path == "direct":
                full_url = checkOffLine(direct(link))

        else: full_url = "special://home/addons/plugin.video.kenhtrongnuoc/off.mp4"

        d_progress.close()

        #dialog = xbmcgui.Dialog()
        #dialog.textviewer('Plot',full_url )

        #ok = xbmc.Player().play(full_url)
        return xbmc.Player().play(full_url)


def Init():
        construct_menu("root")

if mode==None:
        Init()
elif mode==1:
        play_link(chn, src)
        #import web_pdb; web_pdb.set_trace()
elif mode==2:
        construct_menu(chn)
        
