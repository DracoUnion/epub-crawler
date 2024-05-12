# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, quote_plus
import hashlib
from pyquery import PyQuery as pq
import time
import re
import base64
import random
import traceback
from .util import *
from .config import config

img_pool = ThreadPoolExecutor(5)
RE_DATA_URL = r'^data:image/\w+;base64,'


def set_img_pool(pool):
    global img_pool
    img_pool = pool
    
def get_img_src(el_img):
    url = ''
    for prop in config['imgSrc']:
        url = el_img.attr(prop)
        if url: break
    return url
    
def tr_download_img_safe(*args, **kw):
    try:
        tr_download_img(*args, **kw)
    except:
        traceback.print_exc()


def tr_download_img(url, imgs, picname):
    hash = hashlib.md5(url.encode('utf-8')).hexdigest()
    cache = load_img(hash, config['optiMode'])
    if cache is not None and config['cache']:
        print(f'{url} 已存在于本地缓存中')
        imgs[picname] = cache
        return

    for i in range(config['retry']):
        data = request_retry(
            'GET', url,
            headers=config['headers'],
            check_status=config['checkStatus'],
            retry=config['retry'],
            timeout=config['timeout'],
            proxies=prdict(config['proxy']),
            verify=False,
        ).content
        if is_valid_img(data):
            break
        if i == config['retry'] - 1:
            raise ValueError(f'{url} 图片无法解析')
    print(f'{url} proxy:{config["proxy"]} 下载成功')
    data = opti_img(data, config['optiMode'], config['colors']) or b''
    imgs[picname] = data
    save_img(hash, config['optiMode'], data)
    time.sleep(config['wait'])
    
def process_img_data_url(url, el_img, imgs, **kw):
    if not re.search(RE_DATA_URL, url):
        return False
    picname = hashlib.md5(url.encode('utf-8')).hexdigest() + '.png'
    print(f'pic: {url} => {picname}')
    if picname not in imgs:
        enco_data = re.sub(RE_DATA_URL, '', url)
        data = base64.b64decode(enco_data.encode('utf-8'))
        data = opti_img(data, config['optiMode'], config['colors'])
        imgs[picname] = data
    el_img.attr('src', kw['img_prefix'] + picname)
    return True
    
def process_img(html, imgs, **kw):
    kw.setdefault('img_prefix', 'img/')
    # kw.setdefault('task_idx', 0)
    
    root = pq(html)
    el_imgs = root('img')
    hdls = []
    
    for i in range(len(el_imgs)):
        el_img = el_imgs.eq(i)
        url = get_img_src(el_img)
        if not url: continue
        if process_img_data_url(url, el_img, imgs, **kw):
            continue
        if not url.startswith('http'):
            if kw.get('page_url'):
                url = urljoin(kw.get('page_url'), url)
            else: continue
        
        picname = hashlib.md5(url.encode('utf-8')).hexdigest() + '.png'
        print(f'pic: {url} => {picname}')
        if picname not in imgs:
            '''
            if config['proxyOrder'] == 'squential':
                pr_idx = kw['task_idx'] + 1 + i
                pr = config['proxy'][pr_idx % len(config['proxy'])]
            else:
                pr = random.choice(config['proxy'])
            '''
            hdl = img_pool.submit(tr_download_img_safe, url, imgs, picname)
            hdls.append(hdl)
            
        el_img.attr('src', kw['img_prefix'] + picname)
        el_img.attr('data-original-src', url)
        
    for h in hdls: h.result()
    return root.html()
    
    