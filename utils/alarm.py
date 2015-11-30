#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

EMAIL_SMS_INTERFACE = "http://0.0.0.0:18080/add_email_sms"

class Alarm():
    user = "comos_Bluebird"
    def __init__(self, info, mail_list=None, phone_list=None):
        self.alarmInfo = info
        self.mail_list = mail_list
        self.phone_list = phone_list
        self.result = None

    def send(self):
        data = {}
        data["user"] = self.user
        data["id_title"] = self.alarmInfo.get("id_title", None)
        ##public
        data['email_alert_span_minutes'] = self.alarmInfo.get("email_alert_span_minutes", None)
        data['sms_alert_span_minutes'] = self.alarmInfo.get("sms_alert_span_minutes", None)

        #email info
        data["email_title"] = self.alarmInfo.get("title", None)
        data["email_content"] = self.alarmInfo.get("content", None)
        data["emails"] = self.mail_list
        #sms info
        data["sms_content"] = self.alarmInfo.get("content", None)
        data["phones"] = self.phone_list
        data["coding"] = 'utf8'
        #requests
        rst = requests.post(EMAIL_SMS_INTERFACE, data)
        if not rst.ok and rst.content.count("'success':'1'") != 1:
           raise Exception("alarm error")
        
        self.result = rst.content
        rst.close()

if __name__ == "__main__":
    data = {}
    data['title'] = 'test'
    data['content'] = 'test, how are you doing'
    emails = 'dfff@sina.com'
    phones = '0000000000,00000000'

    alm = Alarm(info = data, mail_list = emails)
    alm.send()
    print alm.result
    
