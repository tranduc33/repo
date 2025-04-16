# -*- coding: utf-8 -*-
# KodiAddon (BUZZR TV Live)
# Thanks!
#

#from t1mlib import t1mAddon
import os
import sys
import re
import requests
import urllib.parse
import uuid
import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import xbmcvfs


try:
  import json
except:
  import simplejson as json

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'haingoai.json')

#addon = xbmcaddon.Addon('plugin.video.kenhhaingoai')
USERAGENT = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
httpHeaders = {'User-Agent': USERAGENT,
               'Accept':"application/json, text/javascript, text/html,*/*",
               'Accept-Encoding':'gzip,deflate,sdch',
               'Accept-Language':'en-US,en;q=0.8'
               }

class myAddon():

  def __init__(self):

    self.addon = xbmcaddon.Addon('plugin.video.kenhhaingoai.kd20')
    self.homeDir = self.addon.getAddonInfo('path')
    self.defaultHeaders = httpHeaders
    self.data = self.get_key()
    self.menu_items = self.data['directories']['root']['content']

  
  def get_params(self):

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


  def getAddonMenu(self):

    for menu_item in self.menu_items:
      self.add_chn_link (menu_item['id'])
    #import web_pdb; web_pdb.set_trace()
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


  
  def add_chn_link (self, namex):

    title = self.data['channels'][namex]['title']
    iconimage = self.data['channels'][namex]['logo']
    desc = self.data['channels'][namex]['desc']
    playpath = self.data['channels'][namex]['src']['playpath']
    url = self.data['channels'][namex]['src']['page_url']

    give_url = sys.argv[0]+"?mode=1&chn="+namex+"&title="+title+"&url="+url+"&path="+playpath
    liz = xbmcgui.ListItem(title, offscreen=True)
    liz.setArt({
      "icon": xbmcvfs.translatePath(os.path.join(self.homeDir, 'resources', 'logos', iconimage)),
      "thumb": xbmcvfs.translatePath(os.path.join(self.homeDir, 'resources', 'logos', iconimage))
    })
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=give_url,listitem=liz)



  def playLink(self, chn, title, url, playPath, token):

    if (playPath == "lstv"):
      url = self.parse_gitlab(url, chn, token)
    elif (playPath == "tulix"):
      url = self.parse_tulix(url)
    elif (playPath == "vietmedia"):
      url = self.parse_livestream(url)
    elif (playPath == "vietsky"):
      url = self.parse_vietsky(url) 
    elif (playPath == "vchannel"):
      url = self.parse_vchannel(url)
    else:
      url = self.data['channels'][chn]['src']['page_url']


    # check if channel off live, return off-live video
    #if (requests.get(url, timeout=10)).status_code != 200:
    #  url = "special://home/addons/plugin.video.kenhhaingoai/off.mp4"


    #import web_pdb; web_pdb.set_trace()
    listitem = xbmcgui.ListItem(title)
    xbmc.Player().play(url, listitem)



  def parse_tulix(self, url):

    html = requests.get(url, headers=self.defaultHeaders).text
    return re.compile('source:\"(.+?)\"}', re.DOTALL).search(html).group(1)
  

  
  def parse_livestream(self, url):
      
    #html = requests.get(url, headers=self.defaultHeaders).text
    #import web_pdb; web_pdb.set_trace()
    #return re.compile('\"m3u8_url\":\"(.+?)\",\"secure_m3u8_url\"', re.DOTALL).search(html).group(1)
    try:  
      res = requests.get(url)
    except: 
      return "special://home/addons/plugin.video.kenhhaingoai/off.mp4"
   
    return re.findall(r"\"m3u8_url\":\"(.+?)\",\"secure_m3u8_url\"", res.text)[2]


  
  def parse_vietsky(self, url):
    
    res = requests.get(url)
    return re.findall(r"(https:\/\/.+?m3u8)", res.text)[0]

  
  
  def parse_vchannel(self, url):

    # initialize a session
    #session = requests.Session()

    #try:
    #    r = session.get(url)
    #    p_cookies = session.cookies.get_dict()
    #except:
    #    exit()

    #response = session.post('http://www.vietchannels.com/ajax/getvid.php', headers=self.defaultHeaders, cookies=p_cookies)
    #return response.json()['str']
    #return response.json()['str']

    # Above is old scrape
    #import web_pdb; web_pdb.set_trace()

    res = requests.get(url)
    link = re.findall(r",\'(https:\/\/.+?m3u8.+?)\'\,", res.text)[0]
    #import web_pdb; web_pdb.set_trace()
    return link


  def parse_gitlab(self, url, chn, token):

    #import web_pdb; web_pdb.set_trace()
    return requests.get(url+token).json()

  
  #get key from remote database by device MAC ID, return 0 if MAC not found
  def get_key(self):

    # API endpoint
    url = "https://vietipbox.com/box-api/getChannelList.php"
    
    # retrieve device's mac id
    mac_value = '%012x' % uuid.getnode()
    #mac_value = "18cc18d9574b"
    payload = {
      "macid": mac_value,
      "service": "haingoai"
      }
    #import web_pdb; web_pdb.set_trace()
    try:
      return (requests.get(url, params = payload)).json()

    except:
      dialog = xbmcgui.Dialog()
      dialog.textviewer("Warning!", "Unauthorized Device, Your MAC id:  "+mac_value)
      sys.exit()
      
    # read local json
    #with open(file_path) as f:
    #  data = json.load(f)
    #return data