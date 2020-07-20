"""
 Author: TeamVIB

 Thanks to TVADDONS

 This program was modified from TVADDON's code.

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

import urllib,urllib2,re,xbmcplugin,xbmcgui,os,sys,datetime
import requests
from resources.lib.common_variables import *
from resources.lib.directory import *
from resources.lib.youtubewrapper import *
from resources.lib.watched import * 


fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.YouTube_Vault', 'fanart.jpg'))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.PhimBoYoutube/resources/img', ''))
keyword_path = xbmc.translatePath(os.path.join("special://home/addons/plugin.video.PhimBoYoutube/resources/lib", ""))

KEY = get_key()

if  (str(KEY) == ""):
	macid = get_mac()
	dialog = xbmcgui.Dialog()
	dialog.textviewer("Warning!", "Unauthorized Device, Your MAC id:  "+macid)
	sys.exit()
	

def CATEGORIES():
		addDIR('[COLOR goldenrod]Phim Bo Han Quoc[/COLOR]','url',11,art + 'hq.png')
		addDIR('[COLOR goldenrod]Phim Bo Trung Quoc[/COLOR]','url',12,art + 'tq.png')
		addDIR('[COLOR goldenrod]Phim Bo Hong Kong[/COLOR]','url',10,art + 'hk.png')
		addDIR('[COLOR goldenrod]Phim Bo Dai Loan[/COLOR]','url',13,art + 'tw.png')
		addDIR('[COLOR goldenrod]Phim Bo An Do[/COLOR]','url',14,art + 'ad.png')
		addDIR('[COLOR goldenrod]Phim Bo Thai Lan[/COLOR]','url',15,art + 'tl.png')
		#addDIR('[COLOR goldenrod]Phim Bo Nhat Ban[/COLOR]','url',17,art + 'nb.png')
		addDIR('[COLOR goldenrod]Phim Bo Viet Nam[/COLOR]','url',18,art + 'vn.png')
		#addDIR('[COLOR blue]youtube-dl Control[/COLOR]','url',16,art + 'youtube-dlControl.png')
		logo = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.PhimBoYoutube','logo.png'))
		xbmcgui.Dialog().notification('Phim YouTube','Only in VIET IP BOX',logo,5000,False)
		

def HongKong():
	keyword = "phim+bo+hong+kong"

	# save keyword to file
	write_keyword_to_file(keyword_path, keyword)

	build_dir(keyword, 10, page)

def NhatBan():
	keyword = "phim+nhat+ban"

	# save keyword to file
	write_keyword_to_file(keyword_path, keyword)

	build_dir(keyword, 17, page)
		
def HanQuoc():
	keyword = "phim+bo+han+quoc"

	# save keyword to file
	write_keyword_to_file(keyword_path, keyword)

	build_dir(keyword, 11, page)      
		
def TrungQuoc():
	keyword = "phim+bo+trung+quoc"

	# save keyword to file
	write_keyword_to_file(keyword_path, keyword)	

	build_dir(keyword, 12, page)

def DaiLoan():
	keyword = "phim+bo+dai+loan"

	# save keyword to file
	write_keyword_to_file(keyword_path, keyword)

	build_dir(keyword, 13, page)

def AnDo():
	keyword = "phim+an+do"

	# save keyword to file
	write_keyword_to_file(keyword_path, keyword)

	build_dir(keyword, 14, page)

def ThaiLan():
	keyword = "phim+thai+lan"

	# save keyword to file
	write_keyword_to_file(keyword_path, keyword)

	build_dir(keyword, 15, page)

def VietNam():
	keyword = "phim+bo+viet+nam"

	# save keyword to file
	write_keyword_to_file(keyword_path, keyword)

	build_dir(keyword, 18, page)

def youtube_dl():
	xbmc.executebuiltin("RunAddon(script.module.youtube.dl)")
	

def build_dir(keyword, mode, page):
		if page != 1:
			url_api = BASE_URL+keyword+"%2F"+token+".txt/raw?ref=master&private_token="+KEY
		else:
			url_api = BASE_URL+keyword+"%2Ffirst.txt/raw?ref=master&private_token="+KEY

		raw = requests.get(url_api)
		resp = raw.json()

		try: nextpagetoken = resp["nextPageToken"]
		except: nextpagetoken = ''
		try: availablevideos = resp["pageInfo"]["totalResults"]
		except: availablevideos = 1

		returnedPlaylists = resp["items"]
		totalPlaylists = len(returnedPlaylists)
		#totalpages = int(math.ceil((float(availablevideos)/50)))
		totalpages = 10
		#import web_pdb; web_pdb.set_trace()

		if returnedPlaylists:
			for playlist in returnedPlaylists:
				if ("playlistId" in playlist["id"]):
					playlistid = playlist["id"]["playlistId"]
					rawTitle = playlist["snippet"]["title"]
					title = rawTitle.replace("|", "")

					#import web_pdb; web_pdb.set_trace()
					if ("thumbnails" in playlist["snippet"]):
						thumbnail = playlist["snippet"]["thumbnails"]["high"]["url"]
					#else:
						#thumbnail = art+'movies.png'
						addDIR(title,playlistid,1,thumbnail)
			if totalpages > 1 and (page+1) <= totalpages:
				addDir('[B]'+translate(30010)+'[/B] '+str(page+1)+'/'+str(totalpages),playlistid,mode,os.path.join(artfolder,'next.png'),page+1,1,token=nextpagetoken)


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
url = None
name=None
mode=None
iconimage=None
page = None
token = None
#searchKey = ""


try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except:
	try: 
		mode=params["mode"]
	except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: token=urllib.unquote_plus(params["token"])
except: pass
try: page=int(params["page"])
except: page = 1

print ("Mode: "+str(mode))
print ("URL: "+str(url))
print ("Name: "+str(name))
print ("iconimage: "+str(iconimage))
print ("Page: "+str(page))
print ("Token: "+str(token))

		
def addDIR(name,url,mode,iconimage):

		#u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+name
		ok=True
		liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setProperty('fanart_image', fanart)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
		return ok

def create_directory(dir_path, dir_name=None):
	if dir_name:
		dir_path = os.path.join(dir_path, dir_name)
	dir_path = dir_path.strip()
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	return dir_path



if mode==None or url==None or len(url)<1:
		CATEGORIES()

elif mode==1:
		keyword = get_keyword_from_file(keyword_path)
		return_youtubevideos(name,url,token,page, keyword)

elif mode==5: 
		play_youtube_video(url)

elif mode==6:
		mark_as_watched(url)

elif mode==7:
		removed_watched(url)

elif mode==8:
		add_to_bookmarks(url)

elif mode==9:
		remove_from_bookmarks(url)
		
elif mode==10:
		HongKong()
		
elif mode==11:
		HanQuoc()

elif mode==12:
		TrungQuoc()

elif mode==13:
		DaiLoan()
		
elif mode==14:
		AnDo()

elif mode==15:
		ThaiLan()

elif mode==16:
		youtube_dl()

elif mode==17:
		NhatBan()

elif mode==18:
		VietNam()
				
xbmcplugin.endOfDirectory(int(sys.argv[1]))
