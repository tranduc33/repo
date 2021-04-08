#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import os
import sys
import re




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



#parse http://tvzz.101vn.com/
def parse_101vn(url):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'Accept': '*/*;application/vnd.apple.mpegurl',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,sv;q=0.8,vi;q=0.7',
    }
    response = requests.get(url, headers=headers).text
    
    #convert string to list
    li = list(response.split("\n"))[3]
    return li