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

addon = xbmcaddon.Addon('plugin.video.kenhhaingoai')
mysettings = xbmcaddon.Addon(id='plugin.video.kenhhaingoai')
profile = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile')).decode('utf-8')
home = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path')).decode('utf-8')
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
datafile = xbmc.translatePath(os.path.join(home, 'data.json'))


jsonPath = xbmc.translatePath(os.path.join("special://home/addons/plugin.video.kenhhaingoai/resources", ""))


def get_json():
        with open (datafile,"r") as f:
                return json.load(f)

#import web_pdb; web_pdb.set_trace()


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



def construct_menu(namex):
        
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
        data = get_json()
        #item = xbmcgui.ListItem(chn)
        d_progress = xbmcgui.DialogProgress()
        d_progress.create("Please wait ...", addon.getLocalizedString(30009))

        playPath = data['channels'][chn]['src']['playpath']
        url = data['channels'][chn]['src']['page_url']

        #parse vchannel
        if playPath == "vchannel":
                full_url = checkOffLine(parse_vchannel(url))

        #parse lstv
        elif playPath == "lstv":
                full_url = checkOffLine(parse_lstv(url))

        #parse non-scrape channels
        elif playPath == "non-scrape":
                full_url = checkOffLine(parse_noncsraped(url))

        #parse vietsky
        elif playPath == "vietsky":
                full_url = checkOffLine(parse_vietsky(url))

        #parse vietmedia
        elif playPath == "vietmedia":
                full_url = checkOffLine(parse_vietmedia(url))


        d_progress.close()

        #import web_pdb; web_pdb.set_trace()

        xbmc.Player().play(full_url)
        return



#import web_pdb; web_pdb.set_trace()

mode=None
params=get_params()
#import web_pdb; web_pdb.set_trace()


try:         chn=urllib.unquote_plus(params["chn"])
except: pass
try:         src=urllib.unquote_plus(params["src"])
except: pass
try:         mode=int(params["mode"])
except: pass

#mode=int(params["mode"])
#import web_pdb; web_pdb.set_trace()
        
#get channel json object and save to file
if mode == None:
        with open (datafile,"w") as f:
                json.dump(get_key(), f, ensure_ascii=False, indent=4)

data = get_json()

#import web_pdb; web_pdb.set_trace()

#if mode==None:
construct_menu("root")

if mode==1:
        play_link(chn, src)
