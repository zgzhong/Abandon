import requests
from predict import PhishingClassfier
import cv2
import numpy as np

import shutil
import json

predictor = PhishingClassfier(model_path='phishing_model_vgg16_large_withurl.h5')

success_list = []
failed_list = []

for url in open('phishing_url.txt'):
    req = requests.get('http://localhost:8080', params={'url': url.strip()})
    response = req.json()

    if response['status'] == 'success':
        img = cv2.imread(response['fname'], flags=cv2.IMREAD_COLOR)
        is_phish, score = predictor.judge(img, origin_url=response['origin_url'], landed_url=response['landed_url'])
        response['is_phish'] = is_phish
        response['score'] = score
        success_list.append(response)

        if is_phish:
            shutil.copy(response['fname'], '1/')
            print(response['fname'], 'is phishing! score: ', score)
        else:
            shutil.copy(response['fname'], '0/')
            print(response['fname'], 'not phishing. score: ', score)

    else:
        failed_list.append(response)

with open('out.json', 'w') as f:
    f.write(str({'success': success_list, 'failed': failed_list}))
    # json.dump({'success': success_list, 'failed': failed_list} ,f, default=lambda o: float(o) if isinstance(o, np.int64) else o)