# -*- coding: utf-8 -*-

config = {
    'name': '',
    'url': '',
    'link': '',
    'title': 'title',
    'content': '',
    'remove': '',
    'retry': 10,
    'wait': 0,
    'encoding': 'utf-8',
    'credit': True,
    'headers': {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
    },
    'list': [],
    'optiMode': 'quant',
    'colors': 8,
    'timeout': None,
    'connTimeout': 10,
    'readTimeout': 60,
	'imgSrc': ['data-src', 'data-original-src', 'src'],
    'proxy': [None],
    'proxyOrder': 'sequential',
    'textThreads': 8,
    'imgThreads': 24,
    'external': None,
    'checkStatus': True,
    'checkBlank': True,
    'cache': True,
    'waitContent': False,
    'debug': False,
    'selenium': False,
    'sizeLimit': '50m',
}