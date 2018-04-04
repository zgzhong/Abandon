"""
分析url的特征
"""

import socket
from urllib.parse import urlsplit
from collections import Counter
import logging


logger = logging.getLogger(__name__)


class URLFeature(object):
    def __init__(self, url):
        self.url = url
        self._setup()

    def _setup(self):
        self.url_splited = urlsplit(self.url)
        self.use_ip = self._domain_is_ip()
        self.url_len = len(self.url)
        self.at_symbol = '@' in self.url
        self.domain_dash_cnt = Counter(self.url_splited)['-']
        self.domain_seg_num = len(self.url_splited.netloc.split('.')) if self.use_ip else None

        if self.url_splited.scheme == 'https':
            self.double_slash_redirect = (self.url.rfind('//') > 6)
        elif self.url_splited.scheme == 'http':
            self.double_slash_redirect = (self.url.rfind('//') > 5)

    def to_dict(self):
        return {
            'use_ip': self.use_ip,
            'url_len': self.url_len,
            'at_symbol': self.at_symbol,
            'domain_dash_cnt': self.domain_dash_cnt,
            'domain_seg_num': self.domain_seg_num,
            'double_slash_redirect': self.double_slash_redirect,
        }

    def _domain_is_ip(self):
        netloc = self.url_splited.netloc
        port_index = netloc.rfind(':')
        if port_index != -1:
            netloc = netloc[:port_index]

        self.host = netloc

        logger.debug('The netloc: {}'.format(netloc))

        try:
            socket.inet_aton(netloc)
            return True
        except OSError:
            return False



if __name__ == '__main__':
    test_url = [ URLFeature(x)._domain_is_ip() for x in [
        'http://192.168.1.1:8000/index.js',
        'http://192.168.1.1/index.js',
        'http://0xC0.0xA8.0x01.0x01:8000/index.js',
        'http://0xC0.0xA8.0x01.0x01/index.js',
        'http://www.baidu.com:80',
        ]
    ]

    assert list(map(URLFeature._domain_is_ip, test_url)) == [True, True, True, True, False]
