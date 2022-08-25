import frida
import threading
import time
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

device = get_usb_device()
pid = device.spawn([""])
device.resume(pid)
time.sleep(1)  # Without it Java.perform silently fails
session = device.attach(pid)
script = session.create_script(open('E:\\Learning\\School\\Nam4\\DoAnThucTap\\Tool\\js\\test.js').read())
script.load()
input()