#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
 Author: TeamVIB

 Thanks to TVADDONS
 

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
 
"""
import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import xbmcvfs
import os
import re
import sys
import requests
import uuid 


BASE_URL = "https://gitlab.com/api/v4/projects/teamVIB%2FYTphim/repository/files/"

unauthorized_message = "You need to register your device at TDSOLU.com"
#youtube channel
cast = [] #Team members / Cast of the channel. [] if none
tvshowtitle = '' #Name of the show
status = '' #Status of the show
episode_playlists = [''] #List of playlists to consider every integer as the episode number

#addon config
show_live_category = False #hides Live directory if set to False
show_channel_playlists = True #hides channel playlists from main menu if set to False
######################################################################################

addon_id = xbmcaddon.Addon().getAddonInfo('id')
selfAddon = xbmcaddon.Addon(id=addon_id)
datapath = xbmc.translatePath(selfAddon.getAddonInfo('profile')).decode('utf-8')
addonfolder = xbmc.translatePath(selfAddon.getAddonInfo('path')).decode('utf-8')
artfolder = os.path.join(addonfolder,'resources','img')
watchedfolder = os.path.join(datapath,'watched')
msgok = xbmcgui.Dialog().ok
show_uploads_playlist = bool(selfAddon.getSetting('show_uploads_playlist') == 'true')

def makefolders():
	if not os.path.exists(datapath): xbmcvfs.mkdir(datapath)
	if not os.path.exists(watchedfolder):xbmcvfs.mkdir(watchedfolder)
	return

def translate(text):
	return selfAddon.getLocalizedString(text).encode('utf-8')
	
def add_sort_methods():
	sort_methods = [xbmcplugin.SORT_METHOD_LABEL,xbmcplugin.SORT_METHOD_UNSORTED,xbmcplugin.SORT_METHOD_DATE,xbmcplugin.SORT_METHOD_DURATION,xbmcplugin.SORT_METHOD_EPISODE]
	for method in sort_methods:
		xbmcplugin.addSortMethod(int(sys.argv[1]), sortMethod=method)
	return 

def switching_key():
	for api_key in key:
		url_api = 'https://www.googleapis.com/youtube/v3/search?part=snippet&key='+api_key
		code = requests.get(url_api)
		
		if (code.status_code==200): 
			break
	#import web_pdb; web_pdb.set_trace()
	return api_key 
	
def write_keyword_to_file(DirPath, keyword):
	with open (DirPath+"keyword.txt","w") as f:
		f.write(keyword)
	

def get_keyword_from_file(DirPath):
	with open (DirPath+"keyword.txt","r") as f:
		keyword = f.read()
	return keyword

#get device MAC ID
def get_mac():
	return '%012x' % uuid.getnode()
	

#get key from remote database by device MAC ID, return 0 if MAC not found
def get_key():
	url="https://tdsolu.com/validate.php"
	
	mac_value = get_mac()
	myobj = {
		"macid": mac_value,
		"service": "trongnuoc"
		}
	resp = requests.post(url, data = myobj)
	#import web_pdb; web_pdb.set_trace()
	try:
		return resp.json()
	except:
		macid = get_mac()
		dialog = xbmcgui.Dialog()
		dialog.textviewer("Warning!", "Unauthorized Device, Your MAC id:  "+macid)
		sys.exit()




