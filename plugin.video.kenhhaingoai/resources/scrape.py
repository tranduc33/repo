#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import urllib
import re
import json


#parse vchannel
def parse_vchannel(url):
    res = requests.get(url)
    if res:
        return re.findall(r"playfp2\(\'(.+?)\',\'(.+?)\'", res.text)[0][1]
    else:
        return "special://home/addons/plugin.video.kenhhaingoai/off.mp4"

#parse lstv
def parse_lstv(url):
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

