"""
网站特征搜集器
"""

from multiprocessing import Queue, Process
from url_feature import URLFeature
import requests
import json
import logging
import nmap


LOGGING_FORMAT = '[process-%(process)d] [%(asctime)s] [%(levelname)s] - %(message)s'
logging.basicConfig(
    format=LOGGING_FORMAT,
    level=logging.DEBUG,
)


def feature_extract_subproc(url_list, q):
    for idx, item in enumerate(url_list):
        req = requests.get('http://localhost:8080', params={'url': item['url']})
        logging.debug('visit: ', item['url'])
        ret = req.json()
        if ret:
            q.put({'phishtank': item, 'browser': ret})

def feature_collect_subproc(q):

    with open('sites_feature.json', 'w') as f:
        while True:
            item = q.get(True)
            if not item:
                break

            url_feature = URLFeature(item['browser']['landed_url'])
            item['url'] = url_feature.to_dict()
            f.write(json.dumps(item)+',\n')


def scan_port_subproc(q):
    # todo: add function of scanning port
    pass


if __name__ == '__main__':
    queue = Queue()
    phish_list = json.load(open('online-valid.json'))

    extract_proc = Process(target=feature_extract_subproc, args=(phish_list[:10], queue))
    collect_proc = Process(target=feature_collect_subproc, args=(queue,))

    extract_proc.start()
    collect_proc.start()

    extract_proc.join()

    queue.put({}) # put empty item to Queue
    collect_proc.join()