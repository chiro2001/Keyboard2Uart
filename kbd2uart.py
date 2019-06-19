import os
from evdev import InputDevice
from select import select
# import json
import serial
import time
import threading


keycode = {"0": "", "1": "\x1b", "2": "1", "3": "2", "4": "3", "5": "4", "6": "5",
        "7": "6", "8": "7", "9": "8", "10": "9", "11": "0", "12": "-", "13": "=",
        "14": "\b", "15": "\t", "16": "Q", "17": "W", "18": "E", "19": "R",
        "20": "T", "21": "Y", "22": "U", "23": "I", "24": "O", "25": "P",
        "26": "LEFTBRACE", "27": "RIGHTBRACE", "28": "\r", "29": "LEFTCTRL",
        "30": "A", "31": "S", "32": "D", "33": "F", "34": "G", "35": "H",
        "36": "J", "37": "K", "38": "L", "39": ";", "40": "'", "41": "GRAVE",
        "42": "LEFTSHIFT", "43": "\\", "44": "Z", "45": "X", "46": "C",
        "47": "V", "48": "B", "49": "N", "50": "M", "51": ",", "52": ".", "53": "/",
        "54": "RIGHTSHIFT", "55": "KPASTERISK", "56": "LEFTALT", "57": " ", "58": "CAPSLOCK",
        "59": "F1", "60": "F2", "61": "F3", "62": "F4", "63": "F5", "64": "F6", "65": "F7",
        "66": "F8", "67": "F9", "68": "F10", "69": "NUMLOCK", "70": "SCROLLLOCK", "71": "KP7",
        "72": "KP8", "73": "KP9", "74": "KPMINUS", "75": "KP4", "76": "KP5", "77": "KP6",
        "78": "KPPLUS", "79": "KP1", "80": "KP2", "81": "KP3", "82": "KP0", "83": "KPDOT",
        "85": "ZENKAKUHANKAKU", "86": "102ND", "87": "F11", "88": "F12", "89": "RO",
        "90": "KATAKANA", "91": "HIRAGANA", "92": "HENKAN", "93": "KATAKANAHIRAGANA",
        "94": "MUHENKAN", "95": "KPJPCOMMA", "96": "KPENTER", "97": "RIGHTCTRL",
        "98": "KPSLASH", "99": "SYSRQ", "100": "RIGHTALT", "101": "LINEFEED",
        "102": "\x1b\x5b\x31\x7b", "103": "\x1b\x5b\x41", "104": "\x1b\x5b\x35\x7e", "105": "\x1b\x5b\x44",
           "106": "\x1b\x5b\x43",
        "107": "\x1b\x5b\x34\x7e", "108": "\x1b\x5b\x42", "109": "\x1b\x5b\x36\x7e", "110": "INSERT",
           "111": "\x1b\x5b\x33\x7e",
        "112": "MACRO", "113": "MUTE", "114": "VOLUMEDOWN", "115": "VOLUMEUP",
        "116": "POWER", "117": "KPEQUAL", "118": "KPPLUSMINUS", "119": "PAUSE", "120":
            "SCALE", "121": "KPCOMMA", "122": "HANGEUL", "123": "HANJA", "124": "YEN",
        "125": "LEFTMETA", "126": "RIGHTMETA", "127": "COMPOSE", "128": "STOP",
        "129": "AGAIN", "130": "PROPS", "131": "UNDO", "132": "FRONT", "133": "COPY",
        "134": "OPEN", "135": "PASTE", "136": "FIND", "137": "CUT", "138": "HELP",
        "139": "MENU", "140": "CALC", "141": "SETUP", "142": "SLEEP", "143": "WAKEUP",
        "144": "FILE", "145": "SENDFILE", "146": "DELETEFILE", "147": "XFER",
        "148": "PROG1", "149": "PROG2", "150": "WWW", "151": "MSDOS", "152": "COFFEE",
        "153": "ROTATE_DISPLAY", "154": "CYCLEWINDOWS", "155": "MAIL", "156": "BOOKMARKS",
        "157": "COMPUTER", "158": "BACK", "159": "FORWARD", "160": "CLOSECD",
        "161": "EJECTCD", "162": "EJECTCLOSECD", "163": "NEXTSONG", "164": "PLAYPAUSE",
        "165": "PREVIOUSSONG", "166": "STOPCD", "167": "RECORD", "168": "REWIND",
        "169": "PHONE", "170": "ISO", "171": "CONFIG", "172": "HOMEPAGE", "173": "REFRESH",
        "174": "EXIT", "175": "MOVE", "176": "EDIT", "177": "SCROLLUP", "178": "SCROLLDOWN",
        "179": "KPLEFTPAREN", "180": "KPRIGHTPAREN", "181": "NEW", "182": "REDO",
        "183": "F13", "184": "F14", "185": "F15", "186": "F16", "187": "F17",
        "188": "F18", "189": "F19", "190": "F20", "191": "F21", "192": "F22",
        "193": "F23", "194": "F24", "200": "PLAYCD", "201": "PAUSECD", "202": "PROG3",
        "203": "PROG4", "204": "DASHBOARD", "205": "SUSPEND", "206": "CLOSE", "207": "PLAY", "208": "FASTFORWARD", "209": "BASSBOOST", "210": "PRINT", "211": "HP", "212": "CAMERA", "213": "SOUND", "214": "QUESTION", "215": "EMAIL", "216": "CHAT", "217": "SEARCH", "218": "CONNECT", "219": "FINANCE", "220": "SPORT", "221": "SHOP", "222": "ALTERASE", "223": "CANCEL", "224": "BRIGHTNESSDOWN", "225": "BRIGHTNESSUP", "226": "MEDIA", "227": "SWITCHVIDEOMODE", "228": "KBDILLUMTOGGLE", "229": "KBDILLUMDOWN", "230": "KBDILLUMUP", "231": "SEND", "232": "REPLY", "233": "FORWARDMAIL", "234": "SAVE", "235": "DOCUMENTS", "236": "BATTERY", "237": "BLUETOOTH", "238": "WLAN", "239": "UWB", "240": "UNKNOWN", "241": "VIDEO_NEXT", "242": "VIDEO_PREV", "243": "BRIGHTNESS_CYCLE", "244": "BRIGHTNESS_AUTO", "245": "DISPLAY_OFF", "246": "WWAN", "247": "RFKILL", "248": "MICMUTE", "352": "OK", "353": "SELECT", "354": "GOTO", "355": "CLEAR", "356": "POWER2", "357": "OPTION", "358": "INFO", "359": "TIME", "360": "VENDOR", "361": "ARCHIVE", "362": "PROGRAM", "363": "CHANNEL", "364": "FAVORITES", "365": "EPG", "366": "PVR", "367": "MHP", "368": "LANGUAGE", "369": "TITLE", "370": "SUBTITLE", "371": "ANGLE", "372": "ZOOM", "373": "MODE", "374": "KEYBOARD", "375": "SCREEN", "376": "PC", "377": "TV", "378": "TV2", "379": "VCR", "380": "VCR2", "381": "SAT", "382": "SAT2", "383": "CD", "384": "TAPE", "385": "RADIO", "386": "TUNER", "387": "PLAYER", "388": "TEXT", "389": "DVD", "390": "AUX", "391": "MP3", "392": "AUDIO", "393": "VIDEO", "394": "DIRECTORY", "395": "LIST", "396": "MEMO", "397": "CALENDAR", "398": "RED", "399": "GREEN", "400": "YELLOW", "401": "BLUE", "402": "CHANNELUP", "403": "CHANNELDOWN", "404": "FIRST", "405": "LAST", "406": "AB", "407": "NEXT", "408": "RESTART", "409": "SLOW", "410": "SHUFFLE", "411": "BREAK", "412": "PREVIOUS", "413": "DIGITS", "414": "TEEN", "415": "TWEN", "416": "VIDEOPHONE", "417": "GAMES", "418": "ZOOMIN", "419": "ZOOMOUT", "420": "ZOOMRESET", "421": "WORDPROCESSOR", "422": "EDITOR", "423": "SPREADSHEET", "424": "GRAPHICSEDITOR", "425": "PRESENTATION", "426": "DATABASE", "427": "NEWS", "428": "VOICEMAIL", "429": "ADDRESSBOOK", "430": "MESSENGER", "431": "DISPLAYTOGGLE", "432": "SPELLCHECK", "433": "LOGOFF", "434": "DOLLAR", "435": "EURO", "436": "FRAMEBACK", "437": "FRAMEFORWARD", "438": "CONTEXT_MENU", "439": "MEDIA_REPEAT", "440": "10CHANNELSUP", "441": "10CHANNELSDOWN", "442": "IMAGES", "448": "DEL_EOL", "449": "DEL_EOS", "450": "INS_LINE", "451": "DEL_LINE", "464": "FN", "465": "FN_ESC", "466": "FN_F1", "467": "FN_F2", "468": "FN_F3", "469": "FN_F4", "470": "FN_F5", "471": "FN_F6", "472": "FN_F7", "473": "FN_F8", "474": "FN_F9", "475": "FN_F10", "476": "FN_F11", "477": "FN_F12", "478": "FN_1", "479": "FN_2", "480": "FN_D", "481": "FN_E", "482": "FN_F", "483": "FN_S", "484": "FN_B", "497": "BRL_DOT1", "498": "BRL_DOT2", "499": "BRL_DOT3", "500": "BRL_DOT4", "501": "BRL_DOT5", "502": "BRL_DOT6", "503": "BRL_DOT7", "504": "BRL_DOT8", "505": "BRL_DOT9", "506": "BRL_DOT10", "512": "NUMERIC_0", "513": "NUMERIC_1", "514": "NUMERIC_2", "515": "NUMERIC_3", "516": "NUMERIC_4", "517": "NUMERIC_5", "518": "NUMERIC_6", "519": "NUMERIC_7", "520": "NUMERIC_8", "521": "NUMERIC_9", "522": "NUMERIC_STAR", "523": "NUMERIC_POUND", "524": "NUMERIC_A", "525": "NUMERIC_B", "526": "NUMERIC_C", "527": "NUMERIC_D", "528": "CAMERA_FOCUS", "529": "WPS_BUTTON", "530": "TOUCHPAD_TOGGLE", "531": "TOUCHPAD_ON", "532": "TOUCHPAD_OFF", "533": "CAMERA_ZOOMIN", "534": "CAMERA_ZOOMOUT", "535": "CAMERA_UP", "536": "CAMERA_DOWN", "537": "CAMERA_LEFT", "538": "CAMERA_RIGHT", "539": "ATTENDANT_ON", "540": "ATTENDANT_OFF", "541": "ATTENDANT_TOGGLE", "542": "LIGHTS_TOGGLE", "560": "ALS_TOGGLE", "561": "ROTATE_LOCK_TOGGLE", "576": "BUTTONCONFIG", "577": "TASKMANAGER", "578": "JOURNAL", "579": "CONTROLPANEL", "580": "APPSELECT", "581": "SCREENSAVER", "582": "VOICECOMMAND", "583": "ASSISTANT", "592": "BRIGHTNESS_MIN", "593": "BRIGHTNESS_MAX", "608": "KBDINPUTASSIST_PREV", "609": "KBDINPUTASSIST_NEXT", "610": "KBDINPUTASSIST_PREVGROUP", "611": "KBDINPUTASSIST_NEXTGROUP", "612": "KBDINPUTASSIST_ACCEPT", "613": "KBDINPUTASSIST_CANCEL", "614": "RIGHT_UP", "615": "RIGHT_DOWN", "616": "LEFT_UP", "617": "LEFT_DOWN", "618": "ROOT_MENU", "619": "MEDIA_TOP_MENU", "620": "NUMERIC_11", "621": "NUMERIC_12", "622": "AUDIO_DESC", "623": "3D_MODE", "624": "NEXT_FAVORITE", "625": "STOP_RECORD", "626": "PAUSE_RECORD", "627": "VOD", "628": "UNMUTE", "629": "FASTREVERSE", "630": "SLOWREVERSE", "631": "DATA", "632": "ONSCREEN_KEYBOARD", "767": "MAX"}


com = serial.Serial('/dev/ttyS2', 115200, timeout=5)

upper = False
shifted = False

shift_code = {
    '`': '~', '1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&', '8': '*',
    '9': '(', '0': ')', '-': '_', '=': '+', '[': '{', ']': '}', '\\': '|', ';': ':', "'": '"',
    ',': '<', '.': '>', '/': '?'
}


# with open('key_code2.json') as f:
#     keycode = json.load(f)

try_login = False


def write_uart0(string: str):
    os.system('echo %s >> /dev/ttyS0' % string)


def login_thread():
    while True:
        time.sleep(5)
        write_uart0('Kbd2Uart OK. Press SPACE to login.')
        if try_login is True:
            write_uart0('Try to login: root...')
            one_key_login()
            return


def one_key_login():
    char = 'root'
    com.write(char.encode())
    time.sleep(0.5)
    char = 'orangepi'
    com.write(char.encode())


def config_on_boot():
    pass


def detect_input_key(device_name):
    global upper, shifted, try_login
    dev = InputDevice('/dev/input/%s' % device_name)
    while True:
        select([dev], [], [])
        for event in dev.read():
            if event.code == 4 and event.value > 5:
                continue
            if event.code == 0:
                continue
            if str(event.code) not in keycode:
                continue
            char = keycode[str(event.code)]
            val = event.value
            if char == ' ' and val == 1 and try_login is False:
                try_login = True
                continue
            if 'shift' in char.lower() and (val == 1 or val == 0):
                upper = not upper
                if val == 1:
                    shifted = True
                elif val == 0:
                    shifted = False
                continue
            if char == 'CAPSLOCK' and val == 1:
                upper = not upper
                continue
            print("code:%s value:%s " % (event.code, event.value), end='')
            if str(event.code) in keycode:
                print('char:', keycode[str(event.code)])
            else:
                print('')
                continue
            # kbd -> uart:
            if event.value == 1 or event.value == 2:
                if not upper:
                    char = char.lower()
                if shifted and char in shift_code:
                    char = shift_code[char]
                com.write(char.encode())


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
    write_uart0('Use device: %s' % get_device_name())
    t_login = threading.Thread(target=login_thread)
    t_login.setDaemon(True)
    t_login.start()
    detect_input_key(get_device_name())
