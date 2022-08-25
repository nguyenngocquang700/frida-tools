import conf.conf as conf
import pyfiglet
import time
import fridatools
import sys
import os
import pkg_resources
import fridatools as main
# from objection.state.connection import state_connection
# from objection.utils.agent import Agent


# state_connection.gadget_name = "{appPackageName}"
# state_connection.agent = Agent()
# state_connection.agent.inject()
# api = state_connection.get_api()
# api.android_ssl_pinning_disable(False)

# inputCommand = input("input any word to quit!!!")

SSL_JS = './js/bypass-ssl-pinning.js'
FLUTTER_JS = './js/bypass-flutter.js'
CUSTOM_FLUTTER_JS = './js/bypass-custom-flutter.js'

def pass_str():
    str = ''
    return dict(str=str)

def bypass_ssl(appName):
    os.system('cls')
    print(
            "==================================================================="
        )
    print(pyfiglet.figlet_format("Bypass SSL pinning", font = "digital"))
    print(
            "==================================================================="
        )
    print("Choose an option: \n")
    print("     🔅 1. Default ssl pinning bypass")
    print("     🔅 2. Default flutter bypass")
    print("     🔅 3. Custom flutter bypass")
    print("     🔅 4. Load js file")
    print("     🔅 5. Back to main menu")

    choose_options = input("\nEnter option: ")
    if choose_options == "1":
        device = fridatools.get_usb_device()
        pid = device.spawn([appName])
        device.resume(pid)
        time.sleep(1)
        session = device.attach(pid)
        print("success")
        script = fridatools.loadJsFile(session, SSL_JS) 
        sys.stdin.read()
    elif choose_options == "2":
        device = fridatools.get_usb_device()
        pid = device.spawn([appName])
        device.resume(pid)
        time.sleep(1)
        session = device.attach(pid)
        print("success")
        script = fridatools.loadJsFile(session, FLUTTER_JS) 
        sys.stdin.read()
    elif choose_options == "3":
        hexStr = input("\nEnter hex string to bypass: ")
        pattern = ''
        device = fridatools.get_usb_device()
        pid = device.spawn([appName])
        device.resume(pid)
        time.sleep(1)
        session = device.attach(pid)
        print("success")
        script = fridatools.loadJsFile(session, CUSTOM_FLUTTER_JS)
        script.exports.custom_flutter(hexStr)
        # script.post(patterntt)
        sys.stdin.read()
    elif choose_options == "4":
        path = input("\nEnter path js script: ")
        device = fridatools.get_usb_device()
        pid = device.spawn([appName])
        device.resume(pid)
        time.sleep(1)
        session = device.attach(pid)
        print("success")
        script = fridatools.loadJsFile(session, path) 
        sys.stdin.read()
    elif choose_options == "5":
        os.system('cls')
        main.main()