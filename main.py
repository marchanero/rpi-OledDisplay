import os
import sys
if os.name != 'posix':
    sys.exit('platform not supported')
import psutil

from datetime import datetime

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from time import sleep
import socket

#decodigo.com
serial = i2c(port=1, address=0x3C)
#device = ssd1306(serial, rotate=0)
device = ssd1306(serial, width=128, height=32, rotate=0)
#device.capabilities(width=128, height=64, rotate=0)
print("size: " , device.bounding_box)
device.clear()

def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9K'
    >>> bytes2human(100001221)
    '95M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i+1)*10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = int(float(n) / prefix[s])
            return '%s%s' % (value, s)
    return "%sB" % n

def cpu_usage():
    # load average, uptime
    uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
    av1, av2, av3 = os.getloadavg()
    return "Ld:%.1f %.1f %.1f Up: %s" \
            % (av1, av2, av3, str(uptime).split('.')[0])

def mem_usage():
    usage = psutil.virtual_memory()
    return "Mem: %s %.0f%%" \
            % (bytes2human(usage.used), 100 - usage.percent)

def ip_address_f():
    # Get the hostname
    hostname = socket.gethostname()
    # Get the IP address
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def disk_usage(dir):
    usage = psutil.disk_usage(dir)
    return "SD:  %s %.0f%%" \
            % (bytes2human(usage.used), usage.percent)

def network(iface):
    stat = psutil.net_io_counters(pernic=True)[iface]
    return "%s: Tx%s, Rx%s" % \
           (iface, bytes2human(stat.bytes_sent), bytes2human(stat.bytes_recv))


with canvas(device) as draw:
    #draw.rectangle(device.bounding_box, outline="white", fill="black")
    draw.text((10,0), str(ip_address_f()), fill="white")
    draw.text((10, 10), str(cpu_usage()) , fill="white")
    draw.text((10, 20), str(mem_usage()), fill="white")
    


print("*******************************")
print("CPU: ", str(cpu_usage()))   
print("MEM", mem_usage())
print("IP Address:", ip_address_f())
print("Disk usage", disk_usage("/"))
print("network", network('eth0'))
print("*******************************")

sleep(20)