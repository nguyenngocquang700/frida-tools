import conf.conf as conf
import fridatools as main
import pyfiglet
import time
import fridatools
import sys
import os

ROOT_JS = './js/bypass-root.js'
INSECUREBANK = './js/insecurebankRootBypass.js'

def bypass_root(appName):
    os.system('cls')
    print(
            "==================================================================="
        )
    print(pyfiglet.figlet_format("Bypass Root", font = "digital"))
    print(
            "==================================================================="
        )
    print("Choose an option: \n")
    print("     🔅 1. Default root bypass")
    print("     🔅 2. Load js file")
    print("     🔅 3. InsecureBankv2 root bypass")
    print("     🔅 4. Back to main menu")

    choose_options = input("\nEnter option: ")
    if choose_options == "1":
        device = fridatools.get_usb_device()
        pid = device.spawn([appName])
        device.resume(pid)
        time.sleep(1)
        session = device.attach(pid)
        print("success")
        script = fridatools.loadJsFile(session, ROOT_JS) 
        sys.stdin.read()
    elif choose_options == "2":
        path = input("\nEnter path js script: ")
        device = fridatools.get_usb_device()
        pid = device.spawn([appName])
        device.resume(pid)
        time.sleep(1)
        session = device.attach(pid)
        print("success")
        script = fridatools.loadJsFile(session, path) 
        sys.stdin.read()
    elif choose_options == "3":
        device = fridatools.get_usb_device()
        pid = device.spawn([appName])
        device.resume(pid)
        time.sleep(1)
        session = device.attach(pid)
        print("success")
        script = fridatools.loadJsFile(session, INSECUREBANK) 
        sys.stdin.read()
    elif choose_options == "4":
        os.system('cls')
        main.main()