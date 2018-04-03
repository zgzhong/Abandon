from multiprocessing import Process, Queue
import os
import time
import shutil



def convert_json(json):
    if isinstance(json, dict):
        json = [json]

    for item in json:
        key = os.path.basename(item['fname'])
        url_list = [item['origin_url'], item['landed_url']]
        return {key: url_list}


def screenshot_subproc(q):
    import requests
    import json

    json_list = []
    for lino, url in enumerate(open('urls')):
        req = requests.get('http://localhost:8080', params={'url': url.strip()})
        ret = req.json()
        q.put(ret)
        json_list.append(ret)
        print('[screenshot-proc]', lino)

    q.put({})
    with open('hybrid_model.json', 'w') as f:
        f.write(json.dumps(json_list))


def predict_subproc(q):
    import hybrid_model_predict as hmp
    import numpy as np

    while True:
        val = q.get(True)
        if not val:
            break
        if val['status'] == 'success':
            pic_path = val['fname']
            if not os.path.exists(pic_path):
                continue
            print(pic_path)

            url_map = convert_json(val)
            result = hmp.predict(hmp.model, url_map, pic_path)
            predict_type = np.argmax(result)
            predict_score = result[0][predict_type]
            if predict_type == 1 and predict_score >= 0.97:
                shutil.move(pic_path, '1/{:.4f}_{}'.format(result[0][1], os.path.basename(pic_path)))
            else:
                shutil.move(pic_path, '0/{:.4f}_{}'.format(result[0][0], os.path.basename(pic_path)))

            print(pic_path, predict_type, predict_score)


if __name__ == '__main__':
    queue = Queue()

    screenshot_proc = Process(target=screenshot_subproc, args=(queue,))
    predict_proc = Process(target=predict_subproc, args=(queue,))

    predict_proc.start()
    screenshot_proc.start()

    screenshot_proc.join()
    predict_proc.join()
