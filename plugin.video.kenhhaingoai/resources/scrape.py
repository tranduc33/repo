#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import urllib
import re
import json


#parse tulix.tv
def parse_tulix(url):
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
    session = requests.Session()
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,sv;q=0.8,vi;q=0.7',
    }

    try:
        r = session.get(url, headers=headers)
        p_cookies = session.cookies.get_dict()

    except Exception as ex:
        print(ex)
        #pass
        exit()

    headers = {
        'authority': 'vietchannels.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'accept': '*/*',
        'sec-fetch-dest': 'empty',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://vtvgo.vn',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        
        'accept-language': 'en-US,en;q=0.9,sv;q=0.8,vi;q=0.7',
    }


    response = session.post('http://www.vietchannels.com/ajax/getvid.php', headers=headers, cookies=p_cookies)

    jdata = response.json()
    return jdata['str']


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



