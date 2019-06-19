import os
from evdev import InputDevice
from select import select
import json


with open('key_code2.json') as f:
    keycode = json.load(f)


def detect_input_key(device_name):
    dev = InputDevice('/dev/input/%s' % device_name)
    while True:
        select([dev], [], [])
        for event in dev.read():
            print("code:%s value:%s " % (event.code, event.value), end='')
            if event.code in keycode and len(keycode[event.code]) == 1:
                print('char:', keycode[event.code])
            else:
                print('')


def get_device_name():
    li = os.listdir('/sys/class/input')
    for i in li:
        if 'event' not in i:
            continue
        if os.path.exists('/sys/class/input/%s/device/name' % i):
            try:
                with open('/sys/class/input/%s/device/name' % i) as f:
                    data = f.read()
                    if 'keyboard' in data.lower():
                        return i
            except IOError:
                print('Try to read %s ERROR.' % i)


if __name__ == '__main__':
    print(get_device_name())
    detect_input_key(get_device_name())
