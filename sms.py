#coding:utf-8
import urllib
import hashlib
import json

md5 = lambda x: hashlib.md5(x).hexdigest()

def send_sms(phone, msg):
    user = "publish_dev"
    ie = "utf-8"
    level = "1"
    auth = md5(ie + phone  + level  + msg  + 'sssssssssss')
    paras = {"phones": phone, "level":level, "msg":msg, "user":user, "auth":auth}
    url = "http://127.0.0.1/api/sms/send"
    requrl = url + "?" + urllib.urlencode(paras)
    req = urllib.urlopen(requrl)
    returncontent = req.read()
    try:
        ret = json.loads(returncontent)["result"]["status"]["code"] == 0
    except:
        ret = False
    return ret, returncontent

if __name__ == "__main__":
    print send_sms("18900000000", "cesh测试")
    
