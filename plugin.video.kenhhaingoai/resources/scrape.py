#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import urllib
import re
import json


#parse saigontivi
def parse_saigontivi(url):
    res = requests.get(url)
    if res:
        return re.findall(r"source:\"(.+?)\"\}", res.text)[0]
    else:
        return "special://home/addons/plugin.video.kenhhaingoai/off.mp4"


#parse vietmedia
def parse_vietmedia(url):
    res = requests.get(url)
    if res:
        return re.findall(r"\"m3u8_url\":\"(.+?)\",\"secure_m3u8_url\"", res.text)[2]
    else:
        return "special://home/addons/plugin.video.kenhhaingoai/off.mp4"

#parse vchannel
def parse_vchannel(url):
    try:
        res = requests.get(url)
        videoLink = re.findall(r"playfp2\(\'(.+?)\',\'(.+?)\'", res.text)[0][1]
        #import web_pdb; web_pdb.set_trace()
    except:
        return "special://home/addons/plugin.video.kenhhaingoai/off.mp4"
    else:
        try:
            requests.get(videoLink)
            return videoLink
        except:
            return "special://home/addons/plugin.video.kenhhaingoai/off.mp4"
        #if (requests.get(videoLink)).status_code !=  200:
        #    return "special://home/addons/plugin.video.kenhhaingoai/off.mp4"
        #else:
        #    return videoLink
    #import web_pdb; web_pdb.set_trace()


#parse lstv
def parse_lstv(url):
    if (requests.get(url, timeout=10)).status_code !=  200:
        return "special://home/addons/plugin.video.kenhhaingoai/off.mp4"
    else:
        return url


#parse non-scraped channels
def parse_noncsraped(url):
    if (url):
        return url
    else:
        return "special://home/addons/plugin.video.kenhhaingoai/off.mp4"

#parse vietsky
def parse_vietsky(url):
    res = requests.get(url)
    if res:
        return re.findall(r"\"m3u8_url\":\"(.+?m3u8)\?", res.text)[-1]
    else:
        return "special://home/addons/plugin.video.kenhhaingoai/off.mp4"

# return off-line video
def checkOffLine(url):
    if (requests.get(url, timeout=10)).status_code == 200:
        return url
    else:
        return "special://home/addons/plugin.video.kenhtrongnuoc/off.mp4"



