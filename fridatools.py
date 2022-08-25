import frida
import argparse
import pyfiglet
import conf.conf as conf
import modules.server as server
import modules.bypass_root as root
import modules.bypass_ssl_pinning as ssl
import modules.list_classes as classes
import threading
import termcolor
import codecs
import time
import os
import requests
import re
import pkg_resources
from ppadb.device import Device

global session

finished = threading.Event()

def on_message(message, data):
    if 'payload' in message:
        payload = message['payload']
        if isinstance(payload, dict):
            deal_message(payload)
        else:
            print(payload)

def deal_message(payload):
    if 'mes' in payload:
        print(payload['mes'])

    if 'app' in payload:
        app = payload['app']
        lines = app.split('\n')
        print('%-40s\t%-60s\t%-80s' % ('app name', 'bundle identify', 'documents path'))
        for line in lines:
            if len(line):
                arr = line.split('\t')
                if len(arr) == 3:
                    print('%-40s\t%-60s\t%-80s' % (arr[0], arr[1], arr[2]))

    if 'ui' in payload:
        print(payload['ui'])

    if 'finished' in payload:
        finished.set()

def loadJsFile(session, filename):
    source = ''
    with codecs.open(filename, 'r', 'utf-8') as f:
        source = source + f.read()
    script = session.create_script(source)
    script.on('message', on_message)
    script.load()
    return script

def get_js_hook(js_filename):
    return pkg_resources.resource_string("Tool", "js/{}".format(js_filename)).decode("utf-8")

def message_callback(message, data):
    if message["type"] == "send":
        print("🔥 {}".format(message["payload"]))
    else:
        print("🐛 ".format(message))

def load_script_with_device(device, pkg_name, js_file):
    js_code = get_js_hook(js_file)
    device = frida.get_device(device.get_serial_no())
    session = device.attach(pkg_name)
    script = session.create_script(js_code)
    script.on("message", message_callback)
    script.load()
    return script

def listRunningProcess(device):
    processes = device.enumerate_processes()
    processes.sort(key = lambda item : item.pid)
    print('%-6s\t%s' % ('pid', 'name'))
    for process in processes:
        print('%-6s\t%s' % (str(process.pid), process.name))

# def get_frida_server_repo(arch,version='latest'):
#     base_url = 'https://github.com/frida/frida/releases'
#     if version == 'latest':
#         url = base_url
#     else:
#         url = base_url + '/tag/' + version
#     res = requests.get(url)
#     frida_server_path = re.findall(r'\/download\/\d+\.\d+\.\d+\/frida\-server\-15.0.17\d+\-android\-'+arch+'\.xz',res.text)
#     download_url = base_url + frida_server_path[0]
#     filename = frida_server_path[0].split("/")[-1]
#     # check if folder already exists
#     frida_server_bin_folder = os.path.abspath('bin/')
#     frida_server_file_path = os.path.abspath('bin/'+filename)
#     frida_server_download_folder = frida_server_file_path[:-3]
#     ck_frida_server_folder = check_frida_server_version_local(frida_server_download_folder)
#     if ck_frida_server_folder:
#         logger.info("The requested version \'{0}\' is already located locally".format(filename[:-3]))
#     else:
#         # download & write file locally
#         with open('bin/'+filename, "wb") as f:
#             res = requests.get(download_url)
#             f.write(res.content)
#         logger.info("The requested file \'{0}\' was successfully downloaded".format(filename))
#         extract_frida_server_comp(frida_server_file_path)
#     return frida_server_bin_folder, frida_server_download_folder

def get_usb_device():
    dManager = frida.get_device_manager()
    changed = threading.Event()
    def on_changed():
        changed.set()
    dManager.on('changed', on_changed)

    device = None
    while device is None:
        devices = [dev for dev in dManager.enumerate_devices() if dev.type == 'usb']
        if len(devices) == 0:
            print('Waiting for usb device...')
            changed.wait()
            time.sleep(2)
        else:
            device = devices[0]

    dManager.off('changed', on_changed)
    return device

def main():
    # parser = argparse.ArgumentParser(description='frida tools')
    # parser.add_argument(
    #     '-l', '--list', help='list running processes', action='store_true')
    # parser.add_argument(
    #     '-i', '--info', help='list installed app infomation', action='store_true')
    # parser.add_argument('-s', '--ui', metavar='appName',
    #                     help='show UI (only for ios)')
    # parser.add_argument('-d', '--dynhook',
    #                     metavar='appName', help='dynamic hook')
    # parser.add_argument('-t', '--trace', metavar='identifier',
    #                     help='ObjC/java and Module tracer')
    # parser.add_argument('-e', '--enumerate', metavar='identifier',
    #                     help='Collection of functions to enumerate classes and methods')
    # args = parser. parse_args()
    # while conf.ans:
        print(
            "==================================================================="
        )
        print(termcolor.colored(pyfiglet.figlet_format("Frida Tools"), "green", attrs=["bold"]))
        print(
            termcolor.colored("[>]", "red", attrs=["bold"]) +
            termcolor.colored(" Created by : Grizzz", "magenta", attrs=["bold"]))
        print(
            conf.colored("[>]", "red", attrs=["bold"]) + conf.colored(
                f" Version : {conf.version}\n", "magenta", attrs=["bold"]))
        # conf.ver_check()
        print(
            "==================================================================="
        )
        print("Choose an option: \n")
        print("     🎯 1. Bypass root detection")
        print("     🎯 2. Bypass ssl pinning")
        print("     🎯 3. Bypass root and flutter ssl pinning")
        print("     🎯 4. Bypass frida detection")
        print("     🎯 5. Dynamic hooking")
        print("     🎯 6. List processes")
        print("     🎯 7. List classes")
        print("     🎯 8. List app on device")
        print("     🎯 9. Download Frida server")
        print("     🎯 10. Start Frida server")
        print("     🎯 11. Stop Frida server")
        print("     🎯 12. Reboot Frida server")
        conf.ans = input("\nWhat would you like to do? Enter your selection: ")

        if conf.ans == "1":
            appName = input("\nEnter appname: ")
            conf.call_def(root.bypass_root(appName))
        elif conf.ans == "2":
            appName = input("\nEnter appname: ")
            conf.call_def(ssl.bypass_ssl(appName))
        elif conf.ans == "3":
            appName = input("\nEnter appname: ")
            os.system("frida -U --no-pause -l .\\js\\bypass-root.js -l .\\js\\bypass-flutter.js -f" + appName)
        elif conf.ans == "4":
            appName = input("\nEnter appname: ")
            os.system("frida -U --no-pause -l .\\js\\bypass-frida.js -f" + appName)
        elif conf.ans == "5":
            appName = input("\nEnter appname: ")
            dir_js = input("\nEnter js file location: ")
            os.system("frida -U --no-pause -l " + dir_js + " -f" + appName)
        elif conf.ans == "6":
            device = get_usb_device()
            listRunningProcess(device)   
        elif conf.ans == "7":
            appName = input("\nEnter appname: ")
            conf.call_def(classes.list_classes(appName))
        elif conf.ans == "8":
            print("List App on device: \n")
            os.system("frida-ps -Uai")
        elif conf.ans == "9":
            server.update_server()
        elif conf.ans == "10":
            server.start_server()
        elif conf.ans == "11":
            server.stop_server()
        elif conf.ans == "12":
            server.reboot_server()
        else:
            print("You must specify atleast one option to run the application\n") 

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n \n Keyboard Interrupt. ")
    conf.sys.exit()
    # try:
    #     main()
    # except KeyboardInterrupt:
    #     if session:
    #         session. detach()
    #         sys. exit()
    #     else:
    #         pass
    # finally:
    #     pass
