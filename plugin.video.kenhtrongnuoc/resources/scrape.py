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


#parse tvnet
def parse_tvnet(url):
    
    # request page
    session = requests.Session()
    headers = {
      'Connection': 'keep-alive',
      'Cache-Control': 'private',
      'Upgrade-Insecure-Requests': '1',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
      'Accept': '*/*',
      'Accept-Encoding': 'gzip, deflate',
      'Accept-Language': 'en-US,en;q=0.5',
    }

    

    try:
        r = session.get(url, headers=headers, timeout=15)
    except: 
        return "special://home/addons/plugin.video.kenhhaingoai/off.mp4"
    
    path_to_json = re.findall(r"ownURL = \"(.+?)\"", r.text)
    path_to_json = path_to_json[0]

    #import web_pdb; web_pdb.set_trace() 
    
    try:
        session = requests.Session()
        x = session.get(path_to_json, headers=headers, timeout=10)
    except: 
        return "special://home/addons/plugin.video.kenhhaingoai/off.mp4"
 

    x = x.json()[0]   
    m3u = json.dumps(x["url"])
    m3u = m3u.strip('"')

    #split string
    base = m3u.partition("playlist")[0]
    x = session.get(m3u)
    tail = re.findall(r"1280x720\n(.+?)\n", x.text)
    m3u = base + tail[0]
    #import web_pdb; web_pdb.set_trace()
    return m3u



def parse_vtvgo(url):
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
        pass
    
    token = re.findall(r"var token = '(.[^\']*)", r.text)
    
    if not token:
        return None
    
    token = token[0]
    
    time = token.split('.')[0]

    cid = re.findall(r'var id = (\d+)', r.text)
    if cid:
        cid = cid[0]
    else:
        cid = 1
    
    type_id = re.findall(r'''var type_id = '(\d+)''', r.text)
    if type_id:
        type_id = type_id[0]
    else:
        type_id = 1
    
    # Request m3u8
    data = {
        'type_id': type_id,
        'id': cid,
        'time': time,
        'token': token
    }
    headers = {
        'authority': 'vtvgo.vn',
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
        'referer': r.url,
        'accept-language': 'en-US,en;q=0.9,sv;q=0.8,vi;q=0.7',
    }

    
    response = session.post('https://vtvgo.vn/ajax-get-stream', data=data, headers=headers, cookies=p_cookies)
    
    jdata = response.json()
    if 'stream_url' in jdata:
        return jdata['stream_url'][0]
    else:
        print('Fail to get stream url')
        return None


#parse Vcab7
def parse_vcab7(url):
    res = requests.get(url)
    return re.findall(r"source:\"(http://tna6.+?m3u8)\"", res.text)[0]

#parse vchannel
def parse_vchannel(url):
    res = requests.get(url)
    if res:
        return re.findall(r"playfp2\(\'(.+?)\',\'(.+?)\'", res.text)[0][1]
    else:
        return "special://home/addons/plugin.video.kenhtrongnuoc/off.mp4"


#parse non-scraped channels
def direct(url):
    if (url):
        return url
    else:
        return "special://home/addons/plugin.video.kenhhaingoai/off.mp4"


# parse Truyen Hinh Vinh Long. Pull links from GitLab. Links have been scrapped by selenium from local computer
# then upload to GitLab
def parse_thvl(id):
    URL = "https://gitlab.com/api/v4/projects/teamVIB%2Flive/repository/files/live/raw?ref=master&private_token=BmbNpyZoExmdisRo1aYg"
    raw = requests.get(URL)
    resp = raw.json()
    return resp[id]


def parse_for_chunklist_from_gitlab(id):
    #retrieve url
    url = parse_thvl(id)
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