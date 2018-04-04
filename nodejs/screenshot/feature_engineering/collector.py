"""
网站特征搜集器
"""

from multiprocessing import Queue, Process, Lock
from url_feature import URLFeature
import requests
import json
import logging
import nmap


LOGGING_FORMAT = '[process-%(process)d] [%(asctime)s] [%(levelname)s] - %(message)s'
logging.basicConfig(
    format=LOGGING_FORMAT,
    level=logging.INFO,
)


def feature_extract_subproc(url_list, q, q_lock):
    for idx, item in enumerate(url_list):
        req = requests.get('http://localhost:8080', params={'url': item['url']})
        logging.info('visit: {}'.format(item['url']))
        try:
            ret = req.json()
        except Exception as e:
            logging.error(e)
            continue

        if ret:
            q_lock.acquire()
            q.put({'phishtank': item, 'browser': ret})
            q_lock.release()


def feature_collect_subproc(q):
    with open('sites_feature.json', 'w') as f:
        while True:
            item = q.get(True)
            if not item:
                break

            if 'landed_url' in item['browser']:

                landed_url = item['browser']['landed_url']

                url_feature = URLFeature(landed_url)
                item['url'] = url_feature.to_dict()

                logging.info('Begin scan host: {}'.format(url_feature.host))
                nm = nmap.PortScanner()
                item['ports'] =  nm.scan(hosts=url_feature.host, arguments='-n -Pn -F')['scan']
                logging.info('End scan host: {}'.format(url_feature.host))

            f.write(json.dumps(item)+',\n')



if __name__ == '__main__':
    queue = Queue()
    queue_put_lock = Lock()
    phish_list = json.load(open('online-valid.json'))

    extract_proc1 = Process(target=feature_extract_subproc, args=(phish_list[:15000], queue, queue_put_lock))
    extract_proc2 = Process(target=feature_extract_subproc, args=(phish_list[15000:], queue, queue_put_lock))
    collect_proc = Process(target=feature_collect_subproc, args=(queue,))

    extract_proc1.start()
    extract_proc2.start()
    collect_proc.start()

    extract_proc1.join()
    extract_proc2.join()

    queue.put({}) # put empty item to Queue
    collect_proc.join()