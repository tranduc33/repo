# -*- coding: utf-8 -*-
# KodiAddon (BUZZR TV Live)
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
file_path = os.path.join(current_dir, 'trongnuoc.json')


USERAGENT = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
httpHeaders = {'User-Agent': USERAGENT,
               'Accept':"application/json, text/javascript, text/html,*/*",
               'Accept-Encoding':'gzip,deflate,sdch',
               'Accept-Language':'en-US,en;q=0.8'
               }

class myAddon():

  def __init__(self):

    self.addon = xbmcaddon.Addon('plugin.video.kenhtrongnuoc.kd20')
    self.homeDir = self.addon.getAddonInfo('path')
    self.defaultHeaders = httpHeaders
    self.data = self.get_key()
    self.menu_items = self.data['directories']['root']['content']



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
    page_url = self.data['channels'][namex]['src']['page_url']

    give_url = sys.argv[0]+"?mode=1&chn="+namex+"&title="+title+"&url="+page_url+"&path="+playpath
    liz = xbmcgui.ListItem(title)
    liz.setArt({
      "icon": xbmcvfs.translatePath(os.path.join(self.homeDir, 'resources', 'logos', iconimage)),
      "thumb": xbmcvfs.translatePath(os.path.join(self.homeDir, 'resources', 'logos', iconimage))
    })
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=give_url,listitem=liz)



  def playLink(self, chn, title, page_url, playPath, token):
    
    if playPath == "vtv1-5" or playPath =="vtv6-11" or playPath =="vtvgo_local" or playPath =="thvl" \
                    or playPath =="local" or playPath =="regex" or playPath == "selenium-chunklist":
      url = self.parse_gitlab(page_url, chn, token)
    elif (playPath == "hplus"):
      url = self.parse_hplus(page_url) 
    elif (playPath == "vchannel"):
      url = self.parse_vchannel(page_url)
    else:
      url = self.data['channels'][chn]['src']['page_url']

    listitem = xbmcgui.ListItem(title)
    xbmc.Player().play(url, listitem)



  def parse_gitlab(self, url, chn, token):

    resp = requests.get(url+token)

    #import web_pdb; web_pdb.set_trace()

    return resp.json()[chn]



  def parse_hplus(self, url):

    # resp = requests.get(url, headers = self.defaultHeaders)
    # return re.findall(r"getCatchup_admon.+?(https.+?playlist.m3u8)", resp.text)[0]

    html = requests.get(url, headers=self.defaultHeaders).text
    return re.compile('getCatchup_admon.+?(https.+?playlist.m3u8)', re.DOTALL).search(html).group(1)
  

  
  
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

    #Above is old scrape

    res = requests.get(url)
    #link = re.findall(r"(http:\/\/.+?m3u8)\'\,", res.text)[0]
    #import web_pdb; web_pdb.set_trace()
    return re.findall(r",\'(https:\/\/.+?m3u8.+?)\'\,", res.text)[0]

  
  

  #get key from remote database by device MAC ID, return 0 if MAC not found
  def get_key(self):

    # API endpoint
    url = "https://vietipbox.com/box-api/getChannelList.php"
    
    # retrieve device's mac id
    mac_value = '%012x' % uuid.getnode()
    #mac_value = "18cc18d9574b"
    payload = {
      "macid": mac_value,
      "service": "trongnuoc"
      }
    #import web_pdb; web_pdb.set_trace()
    try:
      return (requests.get(url, params = payload)).json()
    except:
      dialog = xbmcgui.Dialog()
      dialog.textviewer("Warning!", "Unauthorized Device, Your MAC id:  "+mac_value)
      sys.exit()
    
    # read local json
    #with open(file_path,"r", encoding="utf-8") as f:
    #  data = json.load(f)
    #return data