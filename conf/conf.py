#!coding:utf8

#rabbitmq monitor config

rmq_partition_monitors = "18900000000" #monitor1
rmq_partition_interval = 5*60 #扫描间隔(s)
basic_auth = {"user": "bluebird",
		"password": "secret"}
