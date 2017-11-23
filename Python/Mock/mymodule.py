import os
import requests

def rm(fname):
    if os.path.isfile(fname):
        os.remove(fname)

class RemovalService(object):
    def rm(self, fname):
        if os.path.isfile(fname):
            os.remove(fname)


# --------- For property mock test --------------- #
class PropertyClass(object):
    @property
    def prop(self):
        req = requests.head("http://www.baidu.com")
        return req.status_codes

def get_status_code():
    instance = PropertyClass()
    return instance.prop