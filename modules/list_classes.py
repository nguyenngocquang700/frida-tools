import conf.conf as conf
import pyfiglet
import time
import fridatools
import sys
import os

CLASS_JS = './js/list-classes.js'

def list_classes(appName):
    os.system('cls')
    print(
            "==================================================================="
        )
    print(pyfiglet.figlet_format("List Classes", font = "digital"))
    print(
            "==================================================================="
        )
    print("All classes of " + appName + "\n")
    device = fridatools.get_usb_device()
    pid = device.spawn([appName])
    device.resume(pid)
    time.sleep(1)
    session = device.attach(pid)
    script = fridatools.loadJsFile(session, CLASS_JS) 
    sys.stdin.read()
    print("List classes successfully!!!")