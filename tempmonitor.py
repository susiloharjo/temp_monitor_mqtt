#!/usr/bin/env python3

import sys, datetime,psutil, paho.mqtt.publish as publish,json
from subprocess import check_output
from re import findall
from time import gmtime, strftime
import os

def get_temp():
    temp = check_output(["vcgencmd","measure_temp"]).decode("UTF-8")
    return(findall("\d+\.\d+",temp)[0])

def bytes2human(n):
# http://code.activestate.com/recipes/577972-disk-usage/
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i+1)*10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n

def getCPUtemperature():
        try:
                res = os.popen('vcgencmd measure_temp').readline()
                tmp1 = res.replace("temp=","")
                tmp1 = tmp1.replace("'","")
                tmp1 = tmp1.replace("C","")
                #print tmp1
                return tmp1
        except:
                return 0

temp1 = int(float(getCPUtemperature()))
#cputemp = 9.0/5.0*temp1
cputemp = temp1

cpupercent = psutil.cpu_percent(interval=1)
vmem = psutil.virtual_memory().percent
diskusage =  psutil.disk_usage('/').percent
disktotal = bytes2human( psutil.disk_usage('/').total )

currtime = strftime("%Y-%m-%d %H:%M:%S")

boottime = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

payload = { 'datetimedatacollected': currtime,
 'cpuusage': cpupercent, 'boottime': boottime,
 'virtualmem': vmem, 'diskusage': diskusage,
 'cputemp': cputemp, 'disktotal': disktotal }

payload_json = json.dumps(payload)
print (payload_json)

persistant_data = True

def publish_message(topic, message):
    print("Publishing to MQTT topic: " + topic)
    print("Message: " + message)

    publish.single(topic, message, hostname="203.153.125.235")

temp = get_temp()
publish_message("gw/temp", " Temperature " + payload_json)
