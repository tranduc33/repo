#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import os
import sys
import re
import json



#parse hplus.com.vn
def parse_hplus(url):
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,sv;q=0.8,vi;q=0.7'
    }
    r = requests.get(url, headers=headers)
    return re.findall(r"getCatchup_admon.+?(https.+?playlist.m3u8)", r.text)[0]



#parse Vcab7
def parse_vcab7(url):
    res = requests.get(url)
    return re.findall(r"source:\"(http://tna6.+?m3u8)\"", res.text)[0]

#parse vchannel
def parse_vchannel(url):
    res = requests.get(url)
    return re.findall(r"(http:\/\/.+?m3u8)\'\,", res.text)[0]


#parse non-scraped channels
def direct(url):
    if (url):
        return url
    else:
        return "special://home/addons/plugin.video.kenhtrongnuoc/off.mp4"




def parse_gitlab(url, chn):
        resp = requests.get(url)
        return resp.json()[chn]


def parse_for_chunklist_from_gitlab(id):
    #retrieve url
    url = parse_local(id)
    base = url.rsplit("/", 1)
    response = requests.get(url, verify=False)
    return base[0] +"/" + re.findall(r"\n(.+?m3u8)", response.text)[0]


# return off-line video
def checkOffLine(url):
    try:
        requests.get(url)
    except:
        return "special://home/addons/plugin.video.kenhtrongnuoc/off.mp4"
    else:
        return url