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

params = dict(urllib.parse.parse_qsl(sys.argv[2].replace('?','',1)))
chn = params.get('chn')
title = params.get('title')
url = params.get('url')
playPath = params.get('path')
mode = int(params.get('mode', '0'))


if mode == 0:
	ma.getAddonMenu()
else:
	#import web_pdb; web_pdb.set_trace()
	d_progress = xbmcgui.DialogProgress()
	d_progress.create("Please wait ...", ma.addon.getLocalizedString(30009))
	ma.playLink(chn, title, url, playPath)
	d_progress.close()