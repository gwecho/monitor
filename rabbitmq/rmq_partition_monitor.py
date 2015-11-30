#!/usr/bin/env python
#coding:utf8
# vim: sw=4 ts=4 sts=4 et

import sys
import os
import time
import datetime

import json
import requests
from requests.auth import HTTPBasicAuth

sys.path.insert(0, os.path.realpath(os.path.join(os.path.realpath(__file__), "..", "..")))
from utils.sms import send_sms
from conf.conf import rmq_partition_monitors, rmq_partition_interval 
from conf.conf import basic_auth

log_path = os.path.realpath(os.path.join(os.path.realpath(__file__), "..", "..", "logs"))
if not os.path.exists(log_path):
    os.mkdir(log_path)
filename, ext = os.path.splitext(os.path.basename(__file__))
log = os.path.realpath(os.path.join(log_path, filename + ".log"))
error_log = os.path.realpath(os.path.join(log_path, filename + ".err"))

def get_rmq_nodes_info(api):
    ret = requests.get("http://" + api + "/api/nodes", 
        auth = HTTPBasicAuth(basic_auth["user"], basic_auth["password"]))
    if not ret.ok:
        with open(error_log, "a") as fp:
            fp.write(datetime.datetime.now().strftime("%D-%H:%M:%S") + " " + ret.content )
        return {}
    return json.loads(ret.content)

def has_partition(nodes_info):
    for node in nodes_info:
        if node['partitions']:
            return True
    return False

def partition_info(nodes_info):
    info = {}
    for node in nodes_info:
        if node['partitions']:
            info[node['name']] = node['partitions']
    return info

def main():
    try:
        assert(len(sys.argv) > 1)
    except AssertionError, e:
        print "usage():" + os.path.basename(__file__) + " ip:port"
        exit(1)
    rmq_api = sys.argv[1]
    with open(log, "a") as fp:
        while(1):
            rmq_nodes_info = get_rmq_nodes_info(rmq_api)
            #rmq_nodes_info.insert(0, {"name":"test", "partitions":["test", "test1"]}) #test alert
            if has_partition(rmq_nodes_info):
                fp.write(datetime.datetime.now().strftime("%D-%H:%M:%S") + "  partitions...\n")
                fp.write(json.dumps(rmq_nodes_info))
                send_sms(rmq_partition_monitors, 
                    "队列分区告警:" + json.dumps(partition_info(rmq_nodes_info)))
            else:
                fp.write(datetime.datetime.now().strftime("%D-%H:%M:%S") + "  no partitions...\n")
            time.sleep(rmq_partition_interval)

if __name__ == "__main__":
    main()
