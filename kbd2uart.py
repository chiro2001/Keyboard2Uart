import os
from evdev import InputDevice
from select import select


def detect_input_key(device_name):
    dev = InputDevice('/dev/input/%s' % device_name)
    while True:
        select([dev], [], [])
        for event in dev.read():
            try:
                print("code:%s value:%s char:%s" % (event.code, event.value, chr(event.code)))
            except Exception as e:
                print("code:%s value:%s char:%s" % (event.code, event.value, e))


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
