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
import sys
import requests
import uuid 
import json



#get device MAC ID
def get_mac():
	return '%012x' % uuid.getnode()
	

#get key from remote database by device MAC ID, return 0 if MAC not found
def get_key():

	url = "https://vietipbox.com/box-api/getChannelList.php"
	
	# retrieve device's mac id
	mac_value = get_mac()
	
	payload = {
		"macid": mac_value,
		"service": "trongnuoc"
		}

	try:

		return (requests.get(url, params = payload)).json()

	except:
		dialog = xbmcgui.Dialog()
		dialog.textviewer("Warning!", "Unauthorized Device, Your MAC id:  "+mac_value)
		sys.exit()




