# -*- coding: utf-8 -*-
# KodiAddon
#
from resources.lib.scraper import myAddon
import re
import sys
import urllib.parse
import xbmcgui
import xbmcaddon

# Start of Module

ma = myAddon()

params = dict(urllib.parse.parse_qsl(sys.argv[2].replace('?','',1), encoding=None))


chn = params.get('chn')
title = params.get('title')
url = params.get('url')

# if use links from gitlab
url = str(url).replace('teamVIB/', 'teamVIB%2F')

playPath = params.get('path')

if (params.get('private_token') != None):
	token = "&private_token="+ str(params.get('private_token'))
else:
	token = ""

mode = int(params.get('mode', '0'))



if mode == 0:
	ma.getAddonMenu()
else:
	#import web_pdb; web_pdb.set_trace()
	d_progress = xbmcgui.DialogProgress()
	d_progress.create("Please wait ...", ma.addon.getLocalizedString(30009))
	ma.playLink(chn, title, url, playPath, token)
	d_progress.close()